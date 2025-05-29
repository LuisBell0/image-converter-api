# Image Converter API 🖼️
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Powered by Pillow](https://img.shields.io/badge/Powered%20by-Pillow-blue?labelColor=red)](https://pillow.readthedocs.io/en/stable/)

---
Image Converter API is a Django REST Framework project for transforming images via a JSON configuration. Authenticated users (with JWT tokens via Djoser) have their processed images saved to Backblaze B2 cloud storage for 24 hours, while anonymous users receive a one-time download link without storage. The main endpoint is implemented as a DRF **ViewSet**`(/api/image/)`, which bundles related actions (list, create, etc.) in one class (see [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)). The API includes common image transformations (grayscale, rotate, resize, etc.) that can be chained via the JSON config. It uses Djoser (with `djangorestframework-simplejwt`) for JWT authentication and provides Swagger/OpenAPI docs at /api/docs/ for easy exploration.

**Repository**: github.com/LuisBell0/image-converter-api

## Table of Contents

- [Features](#features-)
- [Setup](#setup-)
- [Authentication](#authentication-jwt-via-djoser-)
- [Usage](#usage-)
- [Supported Transformations](#supported-transformations-)
- [Full Transform Reference](TRANSFORMS.md)
- [API Documentation](#api-documentation-)
- [Testing](#testing-)
- [Technologies](#technologies-used-)
- [License](#license-)

## Features 🚀

- **Image Transformation**: Upload an image and apply one or more transformations (grayscale, rotate, resize, flip, blur) by specifying a JSON config.  
- **Authentication**: JWT-based authentication using Djoser (with SimpleJWT). Authenticated users store results in the cloud; anonymous users get a download link. Learn more in the [Djoser docs](https://djoser.readthedocs.io/).  
- **Cloud Storage (Backblaze B2)**: Authenticated results are saved in Backblaze B2 (via `django-storages` with S3 API) for 24 hours. Configure your B2 keys in settings (e.g. `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`). See the [django-storages-backblaze-b2 repo](https://github.com/backblaze-b2-samples/django-storages-backblaze-b2).  
- **DRF ViewSet**: The primary `/api/image/` endpoint is a DRF ViewSet, grouping CRUD actions in one class. (see [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)).  
- **API Docs**: Interactive Swagger UI is available at `/api/docs/`, showing all endpoints (via DRF-Spectacular or similar).  
- **Testing**: Comes with unit tests; run them with:  
  ```bash
    python manage.py test
   ```

## Setup ⚙️

⚠️ **Warning**: Setup steps may change as the project evolves. Always check the latest instructions in the repo.
1. **Clone and install**:
    ```bash
    git clone https://github.com/LuisBell0/image-converter-api.git
    cd image-converter-api
    python3 -m venv venv
    venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
2. **Configure environment**:
   - Create a `.env` file or set environment variables for `DJANGO_SECRET_KEY`, database (e.g. `DATABASE_URL`), and Backblaze B2 credentials. For example, in `base.py` you might add:
   ```bash
   AWS_ACCESS_KEY_ID = '<your B2 application key ID>'
   AWS_SECRET_ACCESS_KEY = '<your B2 application key secret>'
   AWS_STORAGE_BUCKET_NAME = '<your B2 bucket name>'
   AWS_S3_REGION_NAME = '<your B2 region (e.g. us-west-001)>'
   ```
   These correspond to Backblaze B2 keys when using `django-storages`
    - Ensure `rest_framework` and `djoser` are in `INSTALLED_APPS`.
3. **Database migrations**:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
4. **Run server**:
    ```bash
    python manage.py runserver
    ```
    By default, the API will be available at `http://127.0.0.1:8000/api/`.

After setup, you can register users and authenticate as described below.
## Authentication (JWT via Djoser) 🔐

This API uses Djoser for user management and JWT authentication. Djoser provides DRF views for registration, login, logout, etc. To use JWT, the project also installs `djangorestframework-simplejwt`.
- **Register a new user**: Send `POST /api/auth/users/` with JSON `{"username":"user", "password":"pass", "re_password":"pass"}"`.
- **Login / Token**: Send `POST /api/auth/jwt/create/` with JSON `{"username":"user", "password":"pass"}`. On success, you receive an **access token**. Djoser’s JWT endpoints include `/jwt/create/`,`/jwt/refresh/`, etc.
- **Authenticated requests**: Include the token in the `Authorization` header: `Authorization: Bearer <access_token>`.
- **Refresh token**: To refresh, use `POST /api/auth/jwt/refresh/` with the refresh token.
- **Anonymous users**: If you don’t supply a token, requests to `/api/image/` will be treated as anonymous (no storage).

Example using HTTPie (or use cURL, Postman, etc.):
```bash
# Register
http POST http://localhost:8000/api/auth/users/ username="alice" password="secret" re_password="secret"
# Obtain JWT token
http POST http://localhost:8000/api/auth/jwt/create/ username="alice" password="secret"
# Response: {"access": "eyJ0eXAiOiJK...", "refresh": "..." }
```
Use the returned `access` token as shown in the usage example below.

## Usage ⚙️

Upload an image and specify transformations in JSON. The primary endpoint is `/api/image/` (a DRF ViewSet):
- **POST /api/image/** – Upload an image and transform it.
- **GET /api/image/** – (Optional) List recent conversions (auth only).
- **GET /api/image/{id}/** – (Optional) Retrieve details or download (if stored).

Here’s an example `POST` using `curl` with a file upload (`image`) and a JSON config (`config`):
```bash
curl -X POST "http://localhost:8000/api/image/" \
     -H "Authorization: Bearer <your_access_token>" \
     -F "image=@/path/to/image.jpg" \
     -F 'config={
           "transformation_name": "transformation_value",
         }'
```
- Replace `<your_access_token>` with the JWT from login.
- The `image` field should be the image file to process.
- The `config` field is a JSON string specifying the filter chain.
- For anonymous requests (no token), the response will include a temporary download URL but no storage. For authenticated requests, the processed image is saved in Backblaze B2 for 24h and the URL is returned in the response.

The endpoint returns a JSON response with details and a link to the transformed image(either a B2 URL or a one-time link).

## Supported Transformations 🖼️

All transforms live under the top-level `"config"` key, which maps transform names to their parameters. There are three parameter styles:
1. **No-parameter transforms**  
   Pass `null`, an empty object `{}`, or an empty array `[]`.  
   ```json
   { "config": { "grayscale": null } }
   ```
2. **Single-parameter transforms**
   Map the transform name to a single value (`number, string, etc.`).
   ```json
   { "config": { "format": "png" } }
   ```
3. **Multi-parameter transforms**
   Map the transform name to an `object` whose keys are parameter `names`.
   ```json
   {
     "config": {
       "resize": {
         "width": 250,
         "height": 300
       }
     }
   }
   ```
**Example: chaining multiple transforms**:
```json
{
  "config": {
    "autocontrast": { "cutoff": 5.0, "preserve_tone": true },
    "rotate": { "angle": 90 },
    "format": "jpeg"
  }
}
```
- autocontrast: multi-param (cutoff, optional ignore, optional preserve_tone)
- rotate: multi-param (angle, optional expand, optional fillColor)
- format: single-param (target format string)

You can mix and match any supported transforms in a single "config" object; they’ll be applied in the order you list them.

The API currently supports the following transformations (with example config):

| Key                  | Parameters                                                                                                                                |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| **autocontrast**     | `{ cutoff(float or tuple of float)`, `ignore(int or list of int, optional)`, `preserve_tone(bool, optional) }`                            |
| **basic_filter**     | `image_filter(str or list of str)`                                                                                                        |
| **border_crop**      | `border(int)`                                                                                                                             |
| **brightness**       | `factor(float or int)`                                                                                                                    |                                                                                                         |
| **color**            | `factor(float or int`                                                                                                                     |
| **contain**          | `{ size(tuple[int, int])`, `method(str, optional) }`                                                                                      |
| **contrast**         | `factor(int or float)`                                                                                                                    |
| **equalize**         | `None or {} or []`                                                                                                                        |
| **expand**           | `{ border(int)`, `fill(int, str, or tuple, optional) }`                                                                                   |
| **flip**             | `None or {} or []`                                                                                                                        |
| **format**           | `new_format(str)`                                                                                                                         |
| **grayscale**        | `None or {} or []`                                                                                                                        |
| **invert**           | `None or {} or []`                                                                                                                        |
| **mirror**           | `None or {} or []`                                                                                                                        |
| **multiband_filter** | `{ size(int)`, `filter_name(str) }`                                                                                                       |
| **pad**              | `{ size(tuple[int, int])`, `method (str, optional)`, `color (int, str, or tuple, optional)`, `centering(tuple[float, float], optional) }` |
| **posterize**        | `bits(int)`                                                                                                                               |
| **rank_filter**      | `{ size(int)`, `filter_name(str) }`                                                                                                       |
| **region_crop**      | `{ left(int)`, `upper(int)`, `right(int)`, `lower(int) }`                                                                                 |
| **resize**           | `{ width(int)`, `height(int) }`                                                                                                           |
| **rotate**           | `{ angle(int or float)`, `expand(bool, optional)`, `fill_color(str, optional) }`                                                          |
| **scale**            | `{ factor(float or int)`, `resample(str, optional) }`                                                                                     |
| **sharpness**        | `factor(int or float)`                                                                                                                    |
| **solarize**         | `threshold(int)`                                                                                                                          |
| **thumbnail**        | `{ size(tuple[float float])`, `resample(str, optional)`, `reducing_gap(float, optional) }`                                                |
| **transpose**        | `transpose_method(str)`                                                                                                                   |

For full parameter details and error cases, see [TRANSFORMS.md](TRANSFORMS.md).

All transforms are powered by Pillow, so for full details on each method you can refer to the official Pillow docs. However, be aware that some operations in this API may have extra constraints or modified behavior—so please consult this documentation first for any API-specific limitations.

## API Documentation 📃

Interactive API documentation is available at the /api/docs/ endpoint. This is generated (e.g. via Swagger/OpenAPI with DRF Spectacular) and lists all available endpoints and models. For example, a typical setup uses something like:
```python
# urls.py
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```
Visiting `http://127.0.0.1:8000/api/docs/` will display a Swagger UI with all routes. This documentation reflects the current API schema and is useful for testing endpoints interactively.

## Testing ✏️

Run the test suite with Django’s test runner:
```bash
python manage.py test
```
Any built-in tests will execute and report coverage of views, serializers, etc. Fix or add tests as needed.

## Technologies Used 🛠️

- **Python 3.x** – Programming language.
- **Django** – Web framework.
- **Django REST Framework (DRF)** – API toolkit for Django.
- **Djoser** – REST auth library providing JWT endpoints.
- **djangorestframework-simplejwt** – JWT authentication for DRF (used by Djoser).
- **Pillow (PIL)** – Image processing library for transformations.
- **django-storages (Backblaze B2 backend)** – To upload images to Backblaze B2 storage.
- **Backblaze B2** – Cloud storage for processed images.
- **drf-spectacular** (or drf-yasg) – API schema generation and Swagger UI for `/api/docs/`.
- **SQLite / PostgreSQL** – Example database backend (configurable via settings).

## License ⚖️

This project is licensed under the [MIT License](LICENSE.md).


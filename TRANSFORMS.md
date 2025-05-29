# Transformation Reference

A complete list of all image-processing transforms, their parameters, constraints, and errors.

---

### autocontrast  
**What it does:**  
Stretches pixel values so the darkest become black and the lightest become white using `PIL.ImageOps.autocontrast`.  

**Parameters:**  
- `cutoff` (float or [float, float])  
  - Percentage of darkest/lightest pixels to ignore (0–100).  
- `ignore` (int or [int], optional)  
  - Pixel values to omit when finding min/max (0–255).  
- `preserve_tone` (bool, optional)  
  - If `True`, attempts to preserve overall tone.  

**Constraints & Errors:**  
- `cutoff` must be a single float ∈ [0,100] or a list/tuple of two such floats.  
  - Invalid → `ValueError("cutoff must be …")`  
- `ignore` values must be ints ∈ [0,255].  
  - Invalid → `ValueError("ignore values must be 0–255")`  
- `preserve_tone` must be a bool.  
  - Invalid → `TypeError`  

### basic_filter  
**What it does:**  
Applies one or more `PIL.ImageFilter` filters in sequence.  

**Parameters:**  
- `image_filter` (str or [str])  
  - Name(s) of filters (e.g. `BLUR`, `EDGE_ENHANCE`).  
  - Valid options: `BLUR`, `CONTOUR`, `DETAIL`, `EDGE_ENHANCE`, `EDGE_ENHANCE_MORE`, `EMBOSS`, `FIND_EDGES`, `SHARPEN`, `SMOOTH`, `SMOOTH_MORE`.  

**Constraints & Errors:**  
- Strings must match attributes of `PIL.ImageFilter`.  
  - Unknown name → `ValueError("Unknown filter: …")`  
- Non-string(s) → `TypeError`  

### border_crop  
**What it does:**  
Crops a uniform border from all sides of the image (inverse of expand).  

**Parameters:**  
- `border` (int)  
  - Number of pixels to remove from each edge (≥ 0).  

**Constraints & Errors:**  
- `border` ≥ 0 and ≤ min(width, height)/2.  
  - Invalid → `ValueError("border must be …")`  
- Non-int → `TypeError`  

### brightness  
**What it does:**  
Adjusts brightness using `PIL.ImageEnhance.Brightness`.  

**Parameters:**  
- `factor` (float or int)  
  - `1.0` = original, `<1.0` = darker, `>1.0` = brighter.  

**Constraints & Errors:**  
- `factor` > 0.  
  - Invalid → `ValueError("factor must be positive")`  
- Non-numeric → `TypeError`  

### color  
**What it does:**  
Adjusts color saturation via `PIL.ImageEnhance.Color`.  

**Parameters:**  
- `factor` (float or int)  
  - `1.0` = original, `<1.0` = less saturated, `>1.0` = more saturated.  

**Constraints & Errors:**  
- `factor` > 0.  
  - Invalid → `ValueError("factor must be positive")`  
- Non-numeric → `TypeError`  

### contain  
**What it does:**  
Resizes the image to fit within a box, preserving aspect ratio (`PIL.ImageOps.contain`).  

**Parameters:**  
- `size` ([int, int])  
  - Target width and height (both > 0).  
- `method` (str, optional)  
  - Resampling filter name.  
  - Valid options: `NEAREST`, `BOX`, `BILINEAR`, `HAMMING`, `BICUBIC`, `LANCZOS`.  

**Constraints & Errors:**  
- `size` values must be > 0.  
  - Invalid → `ValueError("size values must be positive")`  
- `method` must match `PIL.Image.Resampling` constants.  
  - Invalid → `ValueError("Unknown resampling method")`  

### contrast  
**What it does:**  
Modifies contrast using `PIL.ImageEnhance.Contrast`.  

**Parameters:**  
- `factor` (float or int)  
  - `1.0` = original, `<1.0` = lower contrast, `>1.0` = higher contrast.  

**Constraints & Errors:**  
- `factor` > 0.  
  - Invalid → `ValueError("factor must be positive")`  
- Non-numeric → `TypeError`  

### equalize  
**What it does:**  
Equalizes histogram to redistribute pixel values (`PIL.ImageOps.equalize`).  

**Parameters:**  
- None (pass `null`, `{}`, or `[]`).  

**Constraints & Errors:**  
- Any other input → `TypeError("equalize does not accept parameters")`  

### expand  
**What it does:**  
Adds a border around the image (`PIL.ImageOps.expand`).  

**Parameters:**  
- `border` (int)  
  - Pixels to add on each side (≥ 0).  
- `fill` (int, str, or [int], optional)  
  - Color for the new border (e.g. `0`, `"#fff"`, `[255,255,255]`).  

**Constraints & Errors:**  
- `border` ≥ 0.  
  - Invalid → `ValueError("border must be non-negative")`  
- Invalid `fill` type → `TypeError("fill must be int, str, or tuple of ints")`  

### flip  
**What it does:**  
Flips the image top-to-bottom (`PIL.ImageOps.flip`).  

**Parameters:**  
- None (pass `null`, `{}`, or `[]`).  

**Constraints & Errors:**  
- Any parameter → `TypeError("flip does not accept parameters")`  

### format  
**What it does:**  
Converts the image to a new file format (e.g. JPEG, PNG).  

**Parameters:**  
- `new_format` (str)  
  - Valid Pillow format name (`JPEG`, `PNG`, `WEBP`).  

**Constraints & Errors:**  
- Must be one of Pillow’s supported formats.  
  - Invalid → `ValueError("Unsupported format: …")`  

### grayscale  
**What it does:**  
Converts the image to grayscale (`PIL.ImageOps.grayscale`).  

**Parameters:**  
- None (pass `null`, `{}`, or `[]`).  

**Constraints & Errors:**  
- Any parameter → `TypeError("grayscale does not accept parameters")`  

### invert  
**What it does:**  
Inverts pixel values (`PIL.ImageOps.invert`).  

**Parameters:**  
- None (pass `null`, `{}`, or `[]`).  

**Constraints & Errors:**  
- Any parameter → `TypeError("invert does not accept parameters")`  

### mirror  
**What it does:**  
Flips the image left-to-right using `PIL.ImageOps.mirror`.  

**Parameters:**  
- None (pass `null`, `{}`, or `[]`).  

**Constraints & Errors:**  
- Any parameter → `TypeError("mirror does not accept parameters")`
- 
### multiband_filter  
**What it does:**  
Applies a multi-band rank filter using `PIL.ImageFilter.RankFilter` on each channel independently.  

**Parameters:**  
- `radius` (int)  
  - Positive integer window radius (must be ≥ 1).  
- `filter_name` (str)  
  - Name of the rank filter to apply.
  - Valid options: `UNSHARPMASK`, `GAUSSIANBLUR`, `BOXBLUR`.

**Constraints & Errors:**  
- `radius` must be an integer ≥ 1.  
  - Invalid → `ValueError("radius must be a positive integer")`  
  - Non-int → `TypeError("radius must be an integer")`  
- `filter_name` must be a string matching one of the supported rank filters.  
  - Unknown name → `ValueError("Unknown rank filter: …")`  
  - Non-str → `TypeError("filter_name must be a string")`  

### pad  
**What it does:**  
Resizes and pads the image to fit within a given box, preserving aspect ratio (`PIL.ImageOps.pad`).  

**Parameters:**  
- `size` ([int, int])  
  - Target width and height (both > 0).  
- `method` (str)  
  - Resampling filter name.  
  - Valid options: `NEAREST`, `BOX`, `BILINEAR`, `HAMMING`, `BICUBIC`, `LANCZOS`.  
- `color` (int, str, or [int], optional)  
  - Fill color (e.g. `0`, `"#fff"`, `[255,255,255]`).  
- `centering` ([float, float])  
  - Anchor point of the image within the box, each ∈ [0.0, 1.0].  

**Constraints & Errors:**  
- `size` values must be > 0.  
  - Invalid → `ValueError("size values must be positive")`  
- `method` must match `PIL.Image.Resampling` constants.  
  - Invalid → `ValueError("Unknown resampling method")`  
- `color` wrong type or length → `TypeError("color must be int, str, or tuple of ints")`  
- `centering` values not in [0.0,1.0] or wrong length → `ValueError("centering must be two floats 0.0–1.0")`  

### posterize  
**What it does:**  
Reduces the number of bits for each color channel using `PIL.ImageOps.posterize`.  

**Parameters:**  
- `bits` (int)  
  - Number of bits to keep (1–8).  

**Constraints & Errors:**  
- `bits` not in [1–8] → `ValueError("bits must be between 1 and 8")`  
- Non-int → `TypeError("bits must be an integer")`

### rank_filter  
**What it does:**  
Applies a rank filter over a sliding window using `PIL.ImageFilter.RankFilter`.  

**Parameters:**  
- `size` (int)  
  - Positive integer window size (must be ≥ 1).  
- `filter_name` (str)  
  - Name of the rank filter to apply.
  - Valid options: `MIN`, `MEDIAN`, `MAX`.

**Constraints & Errors:**  
- `size` must be an integer ≥ 1.  
  - Invalid → `ValueError("size must be a positive integer")`  
  - Non-int → `TypeError("size must be an integer")`  
- `filter_name` must be a string matching one of the supported rank filters.  
  - Unknown name → `ValueError("Unknown rank filter: …")`  
  - Non-str → `TypeError("filter_name must be a string")`  

### region_crop  
**What it does:**  
Crops a rectangular region from the image using `PIL.Image.crop`.  

**Parameters:**  
- `left`, `upper`, `right`, `lower` (int)  
  - Coordinates of the box edges.  

**Constraints & Errors:**  
- Must satisfy `0 ≤ left < right ≤ width` and `0 ≤ upper < lower ≤ height`.  
  - Invalid → `ValueError("invalid crop box")`  
- Non-int → `TypeError("crop coordinates must be integers")`  

### resize  
**What it does:**  
Resizes the image to specified dimensions using `PIL.Image.resize`.  

**Parameters:**  
- `width`, `height` (int)  
  - New size in pixels, both > 0.  

**Constraints & Errors:**  
- `width` or `height` ≤ 0 → `ValueError("width and height must be positive")`  
- Non-int → `TypeError("width and height must be integers")`  

### rotate  
**What it does:**  
Rotates the image by a given angle using `PIL.Image.rotate`.  

**Parameters:**  
- `angle` (int or float)  
  - Degrees counter-clockwise.  
- `expand` (bool, optional)  
  - If `True`, resize output to hold the whole rotated image.  
- `fill_color` (str, optional)  
  - Color to fill empty areas (e.g. `"#000"`, `"white"`).  

**Constraints & Errors:**  
- Non-numeric `angle` → `TypeError("angle must be a number")`  
- Non-bool `expand` → `TypeError("expand must be a boolean")`  
- Invalid `fillColor` → `ValueError("fillColor must be a valid color string")`  

### scale  
**What it does:**  
Scales the image by a factor using `PIL.ImageOps.scale`.  

**Parameters:**  
- `factor` (int or float)  
  - Scale multiplier, > 0.  
- `resample` (str, optional)  
  - Resampling filter name.  

**Constraints & Errors:**  
- `factor` ≤ 0 → `ValueError("factor must be positive")`  
- Invalid `resample` → `ValueError("Unknown resampling method")`  
- Wrong types → `TypeError`  

### solarize  
**What it does:**  
Inverts all pixel values above a threshold using `PIL.ImageOps.solarize`.  

**Parameters:**  
- `threshold` (int)  
  - Pixel value cutoff (0–255).  

**Constraints & Errors:**  
- `threshold` not in [0–255] → `ValueError("threshold must be 0–255")`  
- Non-int → `TypeError("threshold must be an integer")`  

### thumbnail  
**What it does:**  
Creates a thumbnail by resizing in-place, preserving aspect ratio, using `PIL.Image.thumbnail`.  

**Parameters:**  
- `size` ([float, float])  
  - Max width/height, both > 0.  
- `resample` (str, optional)  
  - Resampling filter name.  
- `reducing_gap` (float, optional)  
  - Minimum reduction for successive passes, > 1.0.  

**Constraints & Errors:**  
- `size` values ≤ 0 → `ValueError("size must be positive")`  
- Invalid `resample` → `ValueError("Unknown resampling method")`  
- `reducing_gap` ≤ 1.0 → `ValueError("reducing_gap must be > 1.0")`  

### transpose  
**What it does:**  
Applies a predefined transpose operation (flip/rotate) using `PIL.Image.Image.transpose`.  

**Parameters:**  
- `transpose_method` (str)  
  - One of `FLIP_LEFT_RIGHT`, `FLIP_TOP_BOTTOM`, `ROTATE_90`, `ROTATE_180`, `ROTATE_270`, `TRANSPOSE`, `TRANSVERSE`.  

**Constraints & Errors:**  
- Invalid method name → `ValueError("Unsupported transpose method")`  
- Non-str → `TypeError("transpose_method must be a string")`

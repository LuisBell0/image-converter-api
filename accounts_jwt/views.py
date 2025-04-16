import requests
from django.http import HttpResponse
from django.views import View


class ActivateUserView(View):
    def get(self, request, uid, token):
        response = requests.post(
            request.build_absolute_uri('/auth/users/activation/'),
            data={'uid': uid, 'token': token}
        )
        if response.status_code == 204:
            return HttpResponse("Account activated successfully.")
        else:
            return HttpResponse("Activation failed.", status=response.status_code)

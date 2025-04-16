from django.urls import path

from accounts_jwt import views

urlpatterns = [
    path('activate/<uid>/<token>/', views.ActivateUserView.as_view(), name='custom-activate'),
]

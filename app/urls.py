from django.urls import path

from .views import CompanyListCreate, CompanyLogin

urlpatterns = [
    path('company/', CompanyListCreate.as_view(), name='company-list-create'),
    path('company/auth/', CompanyLogin.as_view(), name='company-login'),
]

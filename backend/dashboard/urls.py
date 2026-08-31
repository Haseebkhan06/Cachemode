from django.urls import path
from .views import dashboard_home, existing_business_form, new_business_form

urlpatterns = [
    path('', dashboard_home, name='dashboard'),
    path('existing-business/', existing_business_form, name='existing_business_form'),
    path('new-business/', new_business_form, name='new_business_form'),
]

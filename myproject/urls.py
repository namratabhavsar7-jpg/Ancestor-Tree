from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('form/', views.form_page, name='form'),

    path('about/', views.about, name='about'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('contact-info/', views.contact_info, name='contact_info'),
    path('address-details/', views.address_details, name='address_details'),
    path('bank-details/', views.bank_details, name='bank_details'),
    path('upi-details/', views.upi_details, name='upi_details'),
    path('nived-details/', views.nived_details, name='nived_details'),
    path('kuldevi-info/', views.kuldevi_info, name='kuldevi_info'),

]
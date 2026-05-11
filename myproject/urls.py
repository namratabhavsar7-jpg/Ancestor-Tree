from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('form/', views.form_page, name='form'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_page, name='help'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('contact-info/', views.contact_info, name='contact_info'),
    path('address-details/', views.address_details, name='address_details'),
    path('bank-details/', views.bank_details, name='bank_details'),
    path('upi-details/', views.upi_details, name='upi_details'),
    path('nived-details/', views.nived_details, name='nived_details'),
    path('kuldevi-info/', views.kuldevi_info, name='kuldevi_info'),
    path('members/', views.members_list, name='members_list'),
    path('family-tree/', views.family_tree, name='family_tree'),
    path('member/<int:pk>/', views.member_detail, name='member_detail'),
    path('edit-member/<int:pk>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:pk>/', views.delete_member, name='delete_member'),
    path('export-members/', views.export_members_csv, name='export_members'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('identity-info/', views.identity_info, name='identity_info'),
    path('nived-details/', views.nived_details, name='nived_details'),
    path('kuldevi-info/', views.kuldevi_info, name='kuldevi_info'),
    path('search-by-aadhar/', views.search_by_aadhar, name='search_by_aadhar'),
    path('connect-family/', views.connect_family, name='connect_family'),
    path('members/', views.members_list, name='members_list'),
    path('family-tree/', views.family_tree, name='family_tree'),
    path('get-family-json/', views.get_family_json, name='get_family_json'),
    path('member/<int:pk>/', views.member_detail, name='member_detail'),
    path('edit-member/<int:pk>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:pk>/', views.delete_member, name='delete_member'),
    path('export-members/', views.export_members_csv, name='export_members'),

    # AUTH
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # PASSWORD RESET
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
]

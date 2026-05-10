from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('form/', views.form_page, name='form'),

    path('about/', views.about, name='about'),
    path('personal-info/', views.personal_info, name='personal_info'),

]
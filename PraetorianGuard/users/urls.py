#users/urls.py
from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name="home"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('addcompany', views.addcompany, name='addcompany'),
    path('comp_dashboard/<slug:id>', views.comp_dashboard, name='comp_dashboard'),
    path('delete_comp/<slug:id>', views.delete_comp, name='delete_comp'),
    path('verification/<slug:id>', views.verification, name='verification'),
    path('checkDNS', views.checkDNSverification, name='checkDNS'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.addcompany, name='addcompany'),
]
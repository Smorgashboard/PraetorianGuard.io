from django.urls import path
from . import views

urlpatterns = [
    path('phishing', views.phishing, name='phishing'),
    path('emailsinput', views.emailsinput, name='emailsinput'),
    path('success', views.success, name='success'),
]

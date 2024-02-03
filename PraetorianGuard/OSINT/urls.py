from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('scandashboard/<slug>', views.scan_dashboard, name="scandashboard"),
    path('scan',views.scan, name="scan"),
    path('success', views.success, name='success'),
    path('pwCompromised', views.pwCompromised, name='pwCompromised'),
    path('pwScan', views.pwScan, name="pwScan"),
    path('domainCompromised', views.domainCompromised, name="domainCompromised"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('scan',views.scan, name="scan"),
    path('scans_dashboard/<slug:scan_id>', views.scans_dashboard, name='scans_dashboard'),
    path('success', views.success, name='success'),
    path('htmlresults/<slug:scan_id>', views.htmlresults, name='htmlresults'),
]
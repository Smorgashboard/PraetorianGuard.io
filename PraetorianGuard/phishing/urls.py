
from . import views
from django.urls import path, include


urlpatterns = [
    path('emailsinput', views.emailsinput, name='emailsinput'),
    path('success', views.success, name='success'),
    path('pixel.gif', views.pixel, name='pixel.gif'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('tracked', views.tracked, name='tracked'),
    path('campaign_dashboard/<slug:campaign_id>', views.campaign_dashboard, name='campaign_dashboard'),
    path('404', views.uhoh, name='404'),
]

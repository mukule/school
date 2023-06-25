from django.urls import path
from . import views



app_name = 'main'
urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard_admin", views.dashboard_admin, name="dashboard_admin"),
    
]
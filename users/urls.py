from django.urls import path
from .views import login

app_name = 'users'
urlpatterns = [
    path('', login.as_view(), name='index'),
    # Other URL patterns
]

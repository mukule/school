from django.urls import path
from . import views
from .views import teachers


app_name = 'users'
urlpatterns = [
    path('', views.custom_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.custom_logout, name='logout'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
    path('teachers/', teachers.as_view(), name='teachers'),
    path('students/', views.student, name='student'),
     
    # Other URL patterns
]

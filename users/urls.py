from django.urls import path
from . import views
from .views import teachers
from .views import get_filtered_streams


app_name = 'users'
urlpatterns = [
    path('', views.custom_login, name='login'),
    path('student/', views.register, name='register'),
    path('logout', views.custom_logout, name='logout'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
    path('teachers/', teachers.as_view(), name='teachers'),
    path('students/', views.student, name='student'),
    path('create-parent/', views.create_parent, name='create_parent'),
    path('parents', views.parents, name='parents'),
    path('classes/', views.classes, name='classes'),
    path('get_filtered_streams/', get_filtered_streams, name='get_filtered_streams'),

     
    # Other URL patterns
]

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
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('stream/<int:stream_id>/', views.stream_detail, name='stream_detail'),
    path('update-subjects/<int:user_id>/', views.update_subjects, name='update_subjects'),
    path('create-exams/', views.create_exam, name='create_exam'),
    path('exams/', views.exams, name='exams'),
    path('exam/<int:exam_id>/stream/<int:stream_id>/result/', views.exam_result, name='exam_result'),
    path('student/<int:student_id>/exam/<int:exam_id>/result/', views.update_subject_marks, name='student_result'),
    
     
    # Other URL patterns
]

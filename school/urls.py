
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'school'
admin.site.index_title = 'Student Management admin Portal'



urlpatterns = [
    path("", include('users.urls', namespace='users')),
    path("main/", include('main.urls', namespace='main')),
    path('admin/', admin.site.urls),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(ClassName)
admin.site.register(CurriculumActivity)
admin.site.register(Leadership)
admin.site.register(Subject)

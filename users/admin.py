from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(CurriculumActivity)
admin.site.register(Leadership)
admin.site.register(House)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(StudentSubject)
admin.site.register(Result)



class StreamInline(admin.TabularInline):
    model = Stream

class ClassNameAdmin(admin.ModelAdmin):
    inlines = [StreamInline]

admin.site.register(ClassName, ClassNameAdmin)
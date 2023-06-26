from django.contrib import admin
from .models import CustomUser, ClassName, Stream, Parent, Teacher, CurriculumActivity, Leadership, Subject

admin.site.register(CustomUser)
# admin.site.register(ClassName)
# admin.site.register(Stream)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(CurriculumActivity)
admin.site.register(Leadership)
admin.site.register(Subject)
class StreamInline(admin.TabularInline):
    model = Stream

class ClassNameAdmin(admin.ModelAdmin):
    inlines = [StreamInline]

admin.site.register(ClassName, ClassNameAdmin)
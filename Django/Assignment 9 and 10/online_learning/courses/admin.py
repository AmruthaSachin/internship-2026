from django.contrib import admin
from .models import Course, CourseContent
from .models import Course, CourseContent, Enrollment

admin.site.register(Enrollment)
admin.site.register(Course)
admin.site.register(CourseContent)
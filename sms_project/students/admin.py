from django.contrib import admin

from students.models import Course, Post, Profile, Student, Tag


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)

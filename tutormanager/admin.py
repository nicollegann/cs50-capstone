from django.contrib import admin
from .models import User, Tutor, Student, Feedback, Lesson, Schedule, AvailableSlot

# Register your models here.
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Feedback)
admin.site.register(Lesson)
admin.site.register(Schedule)
admin.site.register(AvailableSlot)

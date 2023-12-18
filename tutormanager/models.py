from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.

class User(AbstractUser):
    # inherits from AbstractUser so it already has fields for username, email, password
    USER_TYPES = (
        (1, 'TUTOR'),
        (2, 'STUDENT'),
        (3, 'ADMIN')
    )
    role = models.PositiveSmallIntegerField(choices=USER_TYPES, blank=True, null=True)

    def __str__(self):
        return self.username 


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    acad_level = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "acad_level": self.acad_level,
            "school": self.school
        }

    def username(self):
        return self.user.username

    def get_full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.username


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experience_years = models.IntegerField(default=0)
    bio = models.CharField(max_length=300, blank=True, null=True)
    star = models.ManyToManyField(User, blank=True, related_name="star")

    def serialize(self):
        return {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "experience_years": self.experience_years,
            "bio": self.bio,
        }
    
    def username(self):
        return self.user.username

    def get_full_name(self):
        return self.user.get_full_name()

    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.username


class AvailableSlot(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tutor} has an available lesson slot on {self.date}, {self.time}'


class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f'Lesson schedule for {self.student} by {self.tutor}'


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'Lesson record for {self.student} by {self.tutor}'


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} feedbacked on {self.tutor}'


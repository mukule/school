from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    parent_name = models.CharField(max_length=100, null=True, blank=True)
    parent_contact = models.CharField(max_length=20, null=True, blank=True)
    class_admitted = models.ForeignKey('ClassName', on_delete=models.CASCADE, related_name='admitted_students', null=True, blank=True)
    current_class = models.ForeignKey('ClassName', on_delete=models.CASCADE, related_name='current_students', null=True, blank=True)
    entry_marks = models.FloatField(null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True)
    house = models.CharField(max_length=50, null=True, blank=True)
    subjects = models.ManyToManyField('Subject', related_name='students', null=True, blank=True)
    curriculum_activity = models.ForeignKey('CurriculumActivity', on_delete=models.SET_NULL, null=True, blank=True)
    leadership = models.ForeignKey('Leadership', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    subjects_taught = models.ManyToManyField('Subject', related_name='teachers', blank=True)
    classes_taught = models.ManyToManyField('ClassName', related_name='teachers', blank=True)
    qualifications = models.TextField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=20, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)
    notes = models.TextField(blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ClassName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CurriculumActivity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Leadership(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    date_of_birth = models.DateField(null=True, blank=True)
    class_admitted = models.ForeignKey('ClassName', on_delete=models.CASCADE, related_name='admitted_students', null=True, blank=True)
    entry_marks = models.FloatField(null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True)
    house = models.ForeignKey('House', on_delete=models.SET_NULL, related_name='students', null=True, blank=True)
    stream = models.ForeignKey('Stream', on_delete=models.SET_NULL, related_name='students', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ClassName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=255)
    classes = models.ManyToManyField(ClassName, related_name='exams', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Parent(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parents', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    alternative_phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    subjects_taught = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    classes_taught = models.ManyToManyField(ClassName, related_name='teachers', blank=True)
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


class Stream(models.Model):
    name = models.CharField(max_length=255)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, related_name='streams', null=True, blank=True)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='stream_class_teacher',
                                      null=True, blank=True)
    prefect = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='stream_prefect',
                                null=True, blank=True)
    parent_representative = models.ForeignKey(Parent, on_delete=models.SET_NULL,
                                              related_name='stream_parent_representative',
                                              null=True, blank=True)

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=0)
    prefect = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, related_name='house_prefect',
                                   null=True, blank=True)

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


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks}"


class Result(models.Model):
    student_subject = models.ForeignKey(StudentSubject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return f"{self.student_subject.student} - {self.student_subject.subject}: {self.marks}"
    
class Grade(models.Model):
    grade_name = models.CharField(max_length=10)
    grade_points = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.grade_name

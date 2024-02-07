from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum


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
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks}"
    
class Result(models.Model):
    student_subject = models.ForeignKey(StudentSubject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    grade = models.CharField(max_length=10, null=True, blank=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mean_grade = models.CharField(max_length=10, null=True, blank=True)
    teacher_comments = models.TextField(blank=True)  # Add the field for teacher comments

    def __str__(self):
        return f"{self.student_subject.student} - {self.student_subject.subject}: {self.marks} ({self.exam})"



@receiver(post_save, sender=Result)
def update_result_grade_and_points(sender, instance, **kwargs):
    marks = instance.marks
    instance.grade = calculate_grade(marks)
    instance.points = calculate_points(instance.grade)
    instance.total_points = calculate_total_points(instance.student_subject.student, instance.exam)
    instance.mean_grade = calculate_mean_grade(instance.total_points)
    Result.objects.filter(pk=instance.pk).update(
        grade=instance.grade,
        points=instance.points,
        total_points=instance.total_points,
        mean_grade=instance.mean_grade
    )


def calculate_grade(marks):
    if marks >= 80:
        return 'A'
    elif marks >= 75:
        return 'A-'
    elif marks >= 70:
        return 'B+'
    elif marks >= 65:
        return 'B'
    elif marks >= 60:
        return 'B-'
    elif marks >= 55:
        return 'C+'
    elif marks >= 50:
        return 'C'
    elif marks >= 45:
        return 'C-'
    elif marks >= 40:
        return 'D+'
    elif marks >= 35:
        return 'D'
    elif marks >= 30:
        return 'D-'
    else:
        return 'E'


def calculate_points(grade):
    if grade == 'A':
        return 12
    elif grade == 'A-':
        return 11
    elif grade == 'B+':
        return 10
    elif grade == 'B':
        return 9
    elif grade == 'B-':
        return 8
    elif grade == 'C+':
        return 7
    elif grade == 'C':
        return 6
    elif grade == 'C-':
        return 5
    elif grade == 'D+':
        return 4
    elif grade == 'D':
        return 3
    elif grade == 'D-':
        return 2
    elif grade == 'E':
        return 1
    else:
        return 0


def calculate_total_points(student, exam):
    # Calculate the total points for a student in all subjects within an exam
    result_qs = Result.objects.filter(student_subject__student=student, exam=exam)
    total_points = Decimal('0.00')
    
    for result in result_qs:
        total_points += result.points
    
    return total_points


def calculate_mean_grade(total_points):
    # Calculate the mean grade based on the total points
    if total_points >= 80:
        return 'A'
    elif total_points >= 75:
        return 'A-'
    elif total_points >= 70:
        return 'B+'
    elif total_points >= 65:
        return 'B'
    elif total_points >= 60:
        return 'B-'
    elif total_points >= 55:
        return 'C+'
    elif total_points >= 50:
        return 'C'
    elif total_points >= 45:
        return 'C-'
    elif total_points >= 40:
        return 'D+'
    elif total_points >= 35:
        return 'D'
    elif total_points >= 30:
        return 'D-'
    else:
        return 'E'

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Result

@receiver(pre_save, sender=Result)
def update_result_grade(sender, instance, **kwargs):
    marks = instance.marks
    instance.grade = calculate_grade(marks)

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

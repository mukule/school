from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    id_number = models.CharField(max_length=8, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.username

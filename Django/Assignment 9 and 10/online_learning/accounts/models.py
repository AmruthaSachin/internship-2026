from django.contrib.auth.models import AbstractUser
from django.db import models

import random



class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class EmailOTP(models.Model):

    email = models.EmailField()

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
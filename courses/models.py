from django.db import models
from accounts.models import CustomUser


class Course(models.Model):

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CourseContent(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='contents'
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
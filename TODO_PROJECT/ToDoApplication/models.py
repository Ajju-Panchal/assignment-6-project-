from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    PRIORITY_CHOICES = (
        ('1', 'High Priority'),
        ('2', 'Medium Priority'),
        ('3', 'Low Priority')
    )
    task_title = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=3)

    def __str__(self):
        return self.task_title

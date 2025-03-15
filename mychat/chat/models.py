# chat/models.py
from django.db import models
from django.contrib.auth.models import User

# class Topic(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class Message(models.Model):
    room_name = models.CharField(max_length=255)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default='ExampleUser')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}'
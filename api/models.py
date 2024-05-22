from django.db import models

# Create your models here.

class Idea(models.Model):
    title = models.CharField(max_length=255),
    desctiption = models.TextField()

    def __str__(self) -> str:
        return self.title

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=50,unique=True)

class Snippet(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name='tags',null=True, blank=True)

    def __str__(self):
        return self.title



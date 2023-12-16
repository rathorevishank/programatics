from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class UploadImage(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    image_type=models.CharField(max_length=20)
    image_file=models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s {self.image_type} image"
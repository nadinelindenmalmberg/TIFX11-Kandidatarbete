from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='filehandling/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
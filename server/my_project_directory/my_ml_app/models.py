from django.db import models


class UploadedFile(models.Model):
    # Your fields here
    pass  # Replace with your actual model fields

class VideoFile(models.Model):
    video = models.FileField(upload_to='videos/')
    
    # Add other fields as necessary, such as processing status, results, etc.

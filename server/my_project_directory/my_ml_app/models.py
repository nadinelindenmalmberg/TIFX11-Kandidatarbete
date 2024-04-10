from django.db import models

class UploadedFile(models.Model):
    # Assuming each upload might correspond to a video
    file = models.FileField(upload_to='uploads/')
    processed = models.BooleanField(default=False) # To check if the file has been processed

class VideoFile(models.Model):
    video = models.FileField(upload_to='videos/')

# models.py
class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add more fields as needed

    def __str__(self):
        return self.title

from django.db import models

class UploadedFile(models.Model):
    # Assuming each upload might correspond to a video
    file = models.FileField(upload_to='uploads/')
    processed = models.BooleanField(default=False) # To check if the file has been processed

class VideoFile(models.Model):
    video = models.FileField(upload_to='videos/')

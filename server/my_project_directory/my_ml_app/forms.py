from django import forms
from .models import VideoFile


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['video']  # Assuming your model has a 'video' FileField

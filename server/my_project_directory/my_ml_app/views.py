
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadedFile
from .tasks import handle_uploaded_file
from django.http import JsonResponse
import subprocess
from .forms import VideoUploadForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os


# views.py


def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file instance
            instance = UploadedFile(file=request.FILES['file'])
            instance.save()
            
            # Process the uploaded file with a machine learning model asynchronously
            handle_uploaded_file.delay(instance.id)

            # Redirect to the results page, passing the instance id to the URL
            return redirect(reverse('results_page', kwargs={'file_id': instance.id}))
    else:
        form = UploadFileForm()
    
    return render(request, 'my_ml_app/upload.html', {'form': form})

def results_page(request, file_id):
    # Your logic here
    return HttpResponse("This is the results page for file ID: {}".format(file_id))

def home(request):
    return render(request, 'home.html')

# my_ml_app/views.py


@csrf_exempt  # Note: It's important to handle CSRF properly in production
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video']
            save_video(video)
            return HttpResponse("Video uploaded successfully")
    else:
        form = VideoUploadForm()
    return HttpResponse("Upload a video.")

def save_video(video_file):
    upload_dir = '/Users/nadinelindenmalmberg/Documents/GitHub/TIFX11-Kandidatarbete/server/my_project_directory/videos'
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, video_file.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return file_path


def process_video(video_path):

    # Define the full path to the vis.py script
    # Adjust this path according to your project's structure
    script_path = '../../MotionAGFormer/demo/vis.py'

    # Construct the command to run
    command = ['python', script_path, '--video', video_path]

    try:
        # Execute the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # If the script runs successfully, return the stdout
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If the script fails, log the error and return None or handle accordingly
        print(f"Error running script: {e.stderr}")
        return None

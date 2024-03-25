
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


@csrf_exempt  # You can remove this decorator after setting up proper CSRF handling in React
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded video file
            # For now, let's just save it to the model
            form.save()
            return JsonResponse({'message': 'Video uploaded successfully!'}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'message': 'This is the video upload endpoint.'}, status=200)
    

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
    upload_dir = '/Users/nadinelindenmalmberg/Documents/GitHub/TIFX11-Kandidatarbete/MotionAGFormer/demo/video'
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, video_file.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return file_path


def process_video(request, video_filename):
    # Define the path to the uploaded video
    video_path = os.path.join('/Users/nadinelindenmalmberg/Documents/GitHub/TIFX11-Kandidatarbete/MotionAGFormer/demo/video', video_filename)
    
    # Define the path to your script (adjust as necessary)
    script_path = os.path.join('/Users/nadinelindenmalmberg/Documents/GitHub/TIFX11-Kandidatarbete/MotionAGFormer', 'demo', 'vis.py')
    
    # Command to run your script
    command = ['python', script_path, '--video', video_path]
    
    # Execute the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        # If you have output to return, parse it and send it back in the response
        return JsonResponse({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadedFile
from .tasks import handle_uploaded_file
from django.http import JsonResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt
from .forms import VideoUploadForm
from django.http import HttpResponse


# views.py

def handle_uploaded_file(f):
    # Define the specific path where you want to save the uploaded videos
    upload_dir = '/Users/nadinelindenmalmberg/Documents/GitHub/TIFX11-Kandidatarbete/MotionAGFormer/demo/video'
    
    # Ensure the upload directory exists, create it if it doesn't
    os.makedirs(upload_dir, exist_ok=True)

    # Construct the full file path where the file will be saved
    file_path = os.path.join(upload_dir, f.name)

    # Write the uploaded file to the file system
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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

def process_video(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        # Assuming you have a function 'process_video' in your 'test.py' that takes the file path as an argument
        from MotionAGFormer.test import process_video
        result = process_video(uploaded_file.file.path)

        # Return the result as JSON
        return JsonResponse({'result': result})
    except UploadedFile.DoesNotExist:
        return JsonResponse({'error': 'File not found.'}, status=404)


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
    

def run_processing_script(video_path):
    # Use subprocess to call the script as an external process
    result = subprocess.run(
        ['python', 'path_to_your_script/test.py', '--arg', video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout, result.stderr

# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
import os

@csrf_exempt  # You should eventually handle CSRF properly
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('File uploaded successfully')
    else:
        form = UploadFileForm()
    return HttpResponse('Upload a file.')

def handle_uploaded_file(f):
    file_path = os.path.join('uploaded_files', f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path
# my_ml_app/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import VideoUploadForm
import os

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

def test_api(request):
    return JsonResponse({"message": "Hello from Django!"})

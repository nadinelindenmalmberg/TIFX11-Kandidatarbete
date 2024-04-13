
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadedFile, VideoFile
from .tasks import handle_uploaded_file
from django.http import JsonResponse
from .forms import VideoUploadForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from .calculate import calculate_from_json  # Adjust the import path as needed

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
    
    return render(request, 'my_ml_app/upload', {'form': form})

def results_page(request, file_id):
    # Your logic here
    return HttpResponse("This is the results page for file ID: {}".format(file_id))


@csrf_exempt  # Note: It's important to handle CSRF properly in production
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video']
            file_path = save_video(video)
            
            save_video(video)
            video_url = request.build_absolute_uri(settings.MEDIA_URL + 'videos/' + video.name)
            # Use JsonResponse to return the video URL
            return JsonResponse({"success": True, "video_url": video_url})
    else:
        form = VideoUploadForm()
    return JsonResponse({"success": False, "message": "Upload a video."})

def save_video(video_file):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'videos')  # This is the 'videos' subdirectory under MEDIA_ROOT
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, video_file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return file_path


# def results_page(request, file_id):
#     print("i am here")
#     uploaded_file = get_object_or_404(UploadedFile, id=file_id)
#     video_file = uploaded_file.processed_video.last()  # Assuming there might be multiple processed outputs
#     context = {'video_url': video_file.video.url if video_file else None}
#     return render(request, 'my_ml_app/results', context)



def calculation_view(request, filename):
    result = calculate_from_json(filename)
    if result is not None:
        return JsonResponse({"success": True, "result": result})
    else:
        return JsonResponse({"success": False, "error": "File not found or invalid"})

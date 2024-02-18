from django.http import JsonResponse
from .models import File

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file = File.objects.create(file=uploaded_file, name=uploaded_file.name)
        return JsonResponse({'success': True, 'file_id': file.id})
    return JsonResponse({'success': False})

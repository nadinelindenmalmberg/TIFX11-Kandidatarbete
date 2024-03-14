from django import views
from django.urls import path
from .views import test_api
from . import views 

urlpatterns = [
    path('results/<int:file_id>/', views.results_page, name='results_page'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('upload/', views.file_upload, name='upload_page'),  # This correctly references the file_upload view
    path('api/test/', test_api, name='test_api'),
]



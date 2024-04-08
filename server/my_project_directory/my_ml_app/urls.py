from django import views
from django.urls import path
from . import views 
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload_video/', views.upload_video, name='upload_video'),
    path('upload/', views.file_upload, name='upload_page'),  # This correctly references the file_upload view
    path('results/<int:file_id>/', views.results_page, name='results_page'),

]




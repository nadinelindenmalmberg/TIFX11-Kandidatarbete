from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_ml_app/', include('my_ml_app.urls')),
    path('', include('my_ml_app.urls')),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

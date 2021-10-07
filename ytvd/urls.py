from django.contrib import admin
from django.urls import path
from .views import GetVideoURL, DownloadVideo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('video_url', GetVideoURL.as_view(), name="video URL"),
    path('download_video', DownloadVideo.as_view(), name="Download Video"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

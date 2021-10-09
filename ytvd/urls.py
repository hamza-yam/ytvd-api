from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import GetVideoURL, DownloadVideo
from fbvideo.views import fbdownloadMp4, hdvideo, sdvideo


urlpatterns = [
    path('admin/', admin.site.urls),
    path('video_url', GetVideoURL.as_view(), name="video URL"),
    path('download_video', DownloadVideo.as_view(), name="Download Video"),
    # Facebook APP URLs
    path('fb_video', fbdownloadMp4.as_view(), name="Facebook Video"),
    path('download_hd_video', hdvideo.as_view(), name="Download HD Video"),
    path('download_sd_video', sdvideo.as_view(), name="Download SD Video"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

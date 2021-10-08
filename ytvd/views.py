from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
import os
from django.conf import settings
from django.http import FileResponse, HttpResponse


class GetVideoURL(APIView):
    def post(self, request):
        video_url = request.data['url']
        obj = YouTube(video_url)
        obj_streams = obj.streams.filter(progressive=True).all()
        resolutions = []
        for i in obj_streams:
            resolutions.append(i.resolution)
        tile = obj.title
        embed = video_url.replace('watch?v', 'embed/')
        response = {
            'res': resolutions,
            'title': tile,
            'embed': embed
        }
        return Response(response, status=status.HTTP_200_OK)


class DownloadVideo(APIView):
    """
    def post(self, request):
        homedir = os.path.expanduser('~')
        path = homedir + "/Downloads"
        res = request.data['res']
        url = request.data['url']
        obj = YouTube(url)
        obj.streams.get_by_resolution(res).download(path)
        response = "Video Downloded"
        return response
    """

    def post(self, request):
        file_path = settings.MEDIA_ROOT
        res = request.data['res']
        url = request.data['url']
        obj = YouTube(url)
        obj.streams.get_by_resolution(res).download(file_path)
        video_title = obj.title
        # Open file
        with open(settings.MEDIA_ROOT+video_title+'.mp4', 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='application/video.mp4')
        response['Content-Disposition'] = 'attachment; filename=NameOfFile'
        return response

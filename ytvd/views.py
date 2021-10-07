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
    def post(self, request):
        homedir = os.path.expanduser('~')
        path = homedir + "/Downloads"
        res = request.data['res']
        url = request.data['url']
        obj = YouTube(url)
        obj.streams.get_by_resolution(res).download(path)
        response = "Video Downloded"
        return response

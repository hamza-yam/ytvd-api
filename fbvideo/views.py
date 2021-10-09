from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse
from rest_framework import status
from django.conf import settings
from datetime import datetime
import requests
import re


# Create your views here.
class fbdownloadMp4(APIView):
    def post(self, request):
        url = request.data['url']

        # check Link
        if "www.facebook.com" in url:
            url = url
        else:
            try:
                url = requests.head(url).headers['location']
            except:
                return Response({'error': 'Above link is not related to FaceBook'}, status=status.HTTP_400_BAD_REQUEST)
        x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

        # Get HTML
        if x:
            html = requests.get(url).content.decode('utf-8')
        else:
            return Response({'error': 'Something is Wrong'}, status=status.HTTP_400_BAD_REQUEST)

        qualityhd = None
        qualitysd = None

        if 'hd_src:"https' in html:
            qualityhd = "HD"
        if 'sd_src:"https' in html:
            qualitysd = "SD"

        hd = re.search('hd_src:null', html)
        sd = re.search('sd_src:null', html)

        list = []
        theList = [qualityhd, qualitysd, hd, sd]
        for id, val in enumerate(theList):
            if val is not None:
                list.append(id)

        response = {
            "list": list,
            "url": url
        }
        return Response(response, status=status.HTTP_200_OK)


class hdvideo(APIView):
    def post(self, request):
        url = request.data['url']

        # check Link
        if "www.facebook.com" in url:
            url = url
        else:
            try:
                url = requests.head(url).headers['location']
            except:
                return Response({'error': 'Above link is not related to FaceBook'}, status=status.HTTP_400_BAD_REQUEST)
        x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

        # Get HMTL
        if x:
            html = requests.get(url).content.decode('utf-8')
        else:
            return Response({'error': 'Something is Wrong'}, status=status.HTTP_400_BAD_REQUEST)

        quality = "HD"
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
        file_size_req = requests.get(video_url, stream=True)

        block_size = 1024
        file_name = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')

        with open(settings.MEDIA_ROOT + file_name + '.mp4', 'wb') as f:
            for data in file_size_req.iter_content(block_size):
                f.write(data)
            f.close()

        with open(settings.MEDIA_ROOT + file_name + '.mp4', 'rb') as f:
            data = f.read()

        # Download file by Response
        response = HttpResponse(data, content_type='application/video.mp4')
        response['Content-Disposition'] = 'attachment; filename="video.mp4"'
        return response


class sdvideo(APIView):
    def get(self, request):
        url = request.data['url']

        # check Link
        if "www.facebook.com" in url:
            url = url
        else:
            try:
                url = requests.head(url).headers['location']
            except:
                return Response({'error': 'Above link is not related to FaceBook'}, status=status.HTTP_400_BAD_REQUEST)
        x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

        # Get HMTL
        if x:
            html = requests.get(url).content.decode('utf-8')
        else:
            return Response({'error': 'Something is Wrong'}, status=status.HTTP_400_BAD_REQUEST)

        quality = "sd"
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
        file_size_req = requests.get(video_url, stream=True)

        block_size = 1024
        file_name = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')

        with open(settings.MEDIA_ROOT + file_name + '.mp4', 'wb') as f:
            for data in file_size_req.iter_content(block_size):
                f.write(data)
            f.close()

        with open(settings.MEDIA_ROOT + file_name + '.mp4', 'rb') as r:
            data = r.read()

        # Download file by Response
        response = HttpResponse(data, content_type='application/video.mp4')
        response['Content-Disposition'] = 'attachment; filename="video.mp4"'
        return response

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators import gzip
import cv2
import threading
from django.http import StreamingHttpResponse

import torch

import os
import time
import base64
import io
import cv2

import numpy as np
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse

#####
from django.contrib.auth import get_user_model


from django.http import HttpResponse
from .models import Mypothole

from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Mypothole
import os

import urllib
from datetime import datetime
from django.http import HttpResponse, Http404
import mimetypes

from django.core.files import File
from PIL import Image

import time
from django.conf import settings


def detect(request):
    return render(request, 'video/detect.html')

def pothole(request):
    return render(request, 'video/pothole.html')

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')

def gen(camera):
    while True:
        # 웹캠에서 이미지 가져오기
        success, image = camera.read()
        if not success:
            break

        # YOLOv5 모델에서 객체 감지 수행
        results = model(image)

        # 결과를 이미지에 그리기
        for obj in results.xyxy[0]:
            if obj[4] >= 0.8:
                cv2.rectangle(image, (int(obj[0]), int(obj[1])), (int(obj[2]), int(obj[3])), (0, 255, 0), 2)
                cv2.putText(image, f'pothole: {obj[4]:.2f}', (int(obj[0]), int(obj[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    # pothole -> {int(obj[5])}
                if obj[4] >= 0.85: # 사진을 자동으로 찍는 코드
                    img_path = f'./media/video/{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}.jpeg'
                    cv2.imwrite(img_path, image)

        # 이미지를 JPEG로 인코딩하여 바이트 스트림으로 반환
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    # 웹캠 초기화
    camera = cv2.VideoCapture(1)

    # 스트리밍 HTTP 응답 생성
    response = StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    response['Cache-Control'] = 'no-cache'
    return response

######


def display_file(request):
    if request.method == 'GET':

        files = Mypothole.objects.all()
        return render((request, 'mypothole_detail.html', {'files':files}))

def mypothole(request):

    page = request.GET.get('page', '1')  # 페이지
    mypothole_list = Mypothole.objects.order_by('-detect_date')
    paginator = Paginator(mypothole_list, 10)
    page_obj = paginator.get_page(page)
    context = {'mypothole_list': page_obj}

    return render(request, 'video/mypothole_list.html', context)


def mypothole_detail(request, mypothole_id):
    mypothole = get_object_or_404(Mypothole, pk=mypothole_id)

    # 동영상 추가 시 filefield로 바꾸고 추가하기
    #ext = str(mypothole.detect_file).rsplit(".", 1)[1]
    #context = {'mypothole': mypothole, 'is_video': ext in ['mp4', 'avi']}

    context = {'mypothole': mypothole}
    return render(request, 'video/mypothole_detail.html', context)


# 글 삭제
@login_required(login_url='common:login')
def mypothole_delete(request, mypothole_id):
    mypothole = get_object_or_404(Mypothole, pk=mypothole_id)
    if request.user != mypothole.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('video:mypothole_detail', mypothole_id=mypothole.id)
    mypothole.delete()
    return redirect('video:mypothole')

# 보관함에서 신고하기
def mypothole_success(request):
    return render(request, 'video/mypothole_success.html')


# 보관함에서 영상/이미지 다운로드 받기

def file_download(request):

    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('" + message + "');history.back()'</script>")



# 캡처된 이미지를 모델에 적용해서 목록 만들기

def save_images_to_model(request):
    image_path = 'video/'
    image_list = os.listdir(image_path)
    for img in image_list:
        name, extension = os.path.splitext(img)
        if extension.lower() in ['.jpg', '.jpeg', '.png']:
            detect_file = Mypothole(name=name, detect_file=img)
            detect_file.save()

    page = request.GET.get('page', '1')  # 페이지
    mypothole_list = Mypothole.objects.order_by('-detect_date')
    paginator = Paginator(mypothole_list, 10)
    page_obj = paginator.get_page(page)
    context = {'mypothole_list': page_obj}

    return render(request, 'mypothole_list.html', context)


# 새 이미지가 등록될 때마다 업데이트하기 위해 모니터

"""
def monitor_folder():
    # 모니터링 대상 폴더 경로
    folder_path = os.path.join(settings.BASE_DIR, 'video')

    # 이미 처리한 파일명 리스트
    processed_files = []

    while True:
        # 폴더 내의 파일 리스트 가져오기
        file_list = os.listdir(folder_path)

        # 이미 처리한 파일은 스킵
        new_files = [file for file in file_list if file not in processed_files]

        # 새로운 파일이 있으면 처리
        if new_files:
            for file in new_files:
                # 이미지 파일일 경우 모델에 저장
                if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                    image_path = os.path.join(folder_path, file)
                    detect_file = Mypothole(detect_file=image_path)
                    detect_file.save()

                # 이미 처리한 파일 리스트에 추가
                processed_files.append(file)

        # 1초 대기
        time.sleep(1)
"""

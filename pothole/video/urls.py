from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [

    path('', views.detect, name='detect'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('pothole', views.pothole, name='pothole'),


    #####

    # 보관함 리스트
    path('mypothole', views.mypothole, name='mypothole'),

    # 감지 세부사항 보기
    path('<int:mypothole_id>/', views.mypothole_detail, name='mypothole_detail'),

    # 보관함 삭제
    path('video/delete/<int:mypothole_id>/', views.mypothole_delete, name='mypothole_delete'),

    # 신고 완료
    path('success/', views.mypothole_success, name='mypothole_success'),

    # 다운로드
    path('download/', views.file_download, name='file_download'),

]


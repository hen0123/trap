from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.report_list, name='list'),
    # 신고 내용 확인
    path('<int:report_id>/', views.report_detail, name='detail'),

    # 신고하기
    path('create/', views.report_create, name='create'),

    # 신고 완료
    # path('success/', views.report_success, name='success'),

    # 신고 수정
    path('report/modify/<int:report_id>/', views.report_modify, name='report_modify'),

    # 신고 삭제
    path('report/delete/<int:report_id>/', views.report_delete, name='report_delete'),


]

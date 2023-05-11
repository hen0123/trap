from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Report
from .forms import ReportForm

from django.utils import timezone

from django.core.paginator import Paginator


# 신고 게시판 메인 - 신고 목록
def report_list(request):
    page = request.GET.get('page', '1')  # 페이지
    report_list = Report.objects.order_by('-create_date')
    paginator = Paginator(report_list, 10)
    page_obj = paginator.get_page(page)
    context = {'report_list': page_obj}

    return render(request, 'report/report_list.html', context)



def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    context = {'report': report}
    return render(request, 'report/report_detail.html', context)

# 글 작성
@login_required(login_url='common:login')
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.create_date = timezone.now()
            report.save()
            return redirect('report:list')
    else:
        form = ReportForm()
    context = {'form': form}
    return render(request, 'report/report_form.html', context)

#def report_success(request):
#    return render(request, 'report/report_success.html')

# 글 수정
@login_required(login_url='common:login')
def report_modify(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user != report.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('report:detail', report_id=report.id)
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            return redirect('report:detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)
    context = {'form': form}
    return render(request, 'report/report_form.html', context)

# 글 삭제
@login_required(login_url='common:login')
def report_delete(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user != report.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('report:detail', report_id=report.id)
    report.delete()
    return redirect('report:list')

def display_file(request):
    if request.method == 'GET':

        files = Report.objects.all()
        return render((request, 'report_detail.html', {'files':files}))




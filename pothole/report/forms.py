from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['subject', 'x_pos', 'y_pos', 'file', 'content']

        labels = {
            'subject': '제목',
            'x_pos': '위도',
            'y_pos': '경도',
            'file': '첨부파일',
            'content': '신고 내용',
        }



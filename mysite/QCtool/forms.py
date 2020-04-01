from django import forms
from django.core import validators
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

from .models import PatientResult

class UploadFileForm(forms.Form):
    # 文件上传
    instrument = [
                    ("AB", "AB"),
                    ("WATERS", "WATERS"),
                    ("Agilent", "Agilent"),
                    ("daojin", "岛津"),
                ]

    item = [
            (None, ""),
            ("PMNs","血浆MNs"),
            ("UMNs","尿液MNs"),
            ("Ald", "血浆醛固酮"),
            ("UAld", "尿液醛固酮"),
            ("VD","25OH维生素D"),
            ]
    item_name = forms.ChoiceField(label='项目名称', choices=item)
    instrument_type = forms.ChoiceField(label="仪器厂家", choices=instrument)
    instrument_num = forms.CharField(label='仪器编号', max_length=4, validators=[validators.RegexValidator(r"[A-Za-z]{2}(\d){2}", "仪器编号格式错误，请确认！")])
    file = forms.FileField(label='原始数据', validators=[validators.FileExtensionValidator(["txt", "csv", "xml", "docx"], "文件类型错误，请确认！")])
    

class PatientResultForm(forms.Form):
    #病人结果分布

    # def validate_time(start, end):
    #     if start > end:
    #         raise ValidationError(
    #             _('开始时间大于结束时间'))

    data = PatientResult.objects.all()
    instrulist = [(instru, instru) for instru in set(d.instrument for d in data)]
    instrulist.sort()
    instrulist.insert(0, ('all', '所有'))

    instrument_num = forms.ChoiceField(label="仪器编号", choices=instrulist)
    start_time = forms.DateField(label="开始时间", initial=(timezone.now()-timedelta(days=7)).strftime("%Y-%m-%d"), widget=forms.DateTimeInput(attrs={'type':'date'}))
    end_time = forms.DateField(label="结束时间", initial=timezone.now().strftime("%Y-%m-%d") , widget=forms.DateTimeInput(attrs={'type':'date'}))
    # 没有判断开始时间大于结束时间的情况

    # def clean_start_time(self):
    #     start_time = self.cleaned_data['start_time']
    #     end_time = self.cleaned_data['end_time']

    #     if start_time > end_time:
    #         raise ValidationError(_('开始时间大于结束时间'))

    #     return start_time, end_time
        
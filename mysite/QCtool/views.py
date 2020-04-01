import csv
from datetime import timedelta

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.conf import settings
import logging

from .create_table_chart import create_result_chart, createtable
from .forms import PatientResultForm, UploadFileForm
from QCtool.Item.handle import handle_uploaded_file
from .models import PatientResult

logger = logging.getLogger('django')

def file_upload(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            item = request.POST['item_name']
            file = request.FILES['file']
            num = request.POST["instrument_num"].upper()
            types = request.POST["instrument_type"]

            try:
                content = handle_uploaded_file(file, item, num, types)
            except Exception as e:
                raise e
                logger.error("文件名:{}, 错误信息:{}".format(file, e))
                raise Http404("错误信息：{}, 请确认: 1.原始数据与仪器平台是否对应； 2.原始数据格式是否正确。".format(e))
            else:
                logger.info("提交数据:{}".format(file))
                content.update({'file':file})
            
                if item =='PMNs':
                    return render(request, "PMNs.html", content)
                elif item =='UMNs':
                    return render(request, "UMNs.html", content)
                elif item =='Ald':
                    return render(request, "Ald.html", content) 
                elif item =='UAld':
                    return render(request, "UAld.html", content)
                elif item == 'VD':
                    data = PatientResult.objects.filter(instrument=num)
                    chart = create_result_chart(data)
                    content.update({'chart': chart.render_embed()})
                    return render(request, "VD.html", content)
                    
    else:
        form = UploadFileForm()
        
    return render(request, 'form.html', {'form': form})


def show_table_chart(request):

    if request.method == 'POST':

        form = PatientResultForm(request.POST)
        if form.is_valid():
            instru = form.cleaned_data['instrument_num']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time'] + timedelta(days=1) # 等于当天晚上0点

            if end_time >= start_time:
                data = PatientResult.objects.all()

                if instru == 'all':
                    data = data.filter(upload_time__range=(start_time, end_time))
                else:
                    data = data.filter(instrument=instru, upload_time__range=(start_time, end_time))
            
                table = createtable(data)
                chart = create_result_chart(data)

                return render(request, 'table_chart.html', {"form": form,
                                                            "table": table.render_embed(), 
                                                            "chart":chart.render_embed(),
                                                            })
                                                            
    else:
        form = PatientResultForm()

    return render(request, 'table_chart.html', {'form': form})
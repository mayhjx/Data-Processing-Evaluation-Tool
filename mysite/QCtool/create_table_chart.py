# from django.utils.timezone import localtime
from datetime import datetime

import pyecharts.options as opts
from pyecharts.charts import Bar, Grid, Line
from pyecharts.components import Table
from pyecharts.globals import CurrentConfig
from pyecharts.options import ComponentTitleOpts

# pyecharts引用本地静态资源文件设置
CurrentConfig.ONLINE_HOST = "http://10.10.20.1:8080/static/"

def createtable(data):

    # 生成pyecharts表格
    table = Table()
    headers = ["提交日期","仪器编号","板号","样品数量","结果均值","ISD"]
    # rows = [[localtime(d.upload_time).strftime("%Y-%m-%d %X"), d.instrument, d.platenum, d.num, d.mean, d.sd] for d in data]
    rows = [[d.upload_time.strftime("%Y-%m-%d %X"), d.instrument, d.platenum, d.num, d.mean, d.sd] for d in data]
    table.add(headers, rows).set_global_opts(title_opts=ComponentTitleOpts(title="结果分布表"))
    return table

def create_result_chart(data):

    instrulist = list(set(d.instrument for d in data))
    # x = ["{} P{}".format(localtime(d.upload_time).strftime("%Y-%m-%d %X"), d.platenum) for d in data]
    x = ["{} P{}".format(d.upload_time.strftime("%Y-%m-%d %X"), d.platenum) for d in data]

    # 均值直方图
    b = Bar(init_opts=opts.InitOpts(width='1900px'))
    b.add_xaxis(x)
    for instru in instrulist:
        mean = get_mean(data, instru)
        b.add_yaxis(instru, mean)
    b.set_global_opts(title_opts=opts.TitleOpts(title="结果mean图"))

    # sd折线图
    l = Line(init_opts=opts.InitOpts(width='1900px'))
    l.add_xaxis(x)
    for instru in instrulist:
        sd = get_sd(data, instru)
        l.add_yaxis(instru, sd, is_connect_nones=True)
    l.set_global_opts(title_opts=opts.TitleOpts(title="结果sd图", pos_top='48%'))

    grid = Grid(init_opts=opts.InitOpts(width='1900px'))
    grid.add(b, grid_opts=opts.GridOpts(pos_bottom='60%'))
    grid.add(l, grid_opts=opts.GridOpts(pos_top='60%'))
    
    return grid

def get_sd(data, target_instrument):

    # 获取不同仪器的sd值
    result = []
    timelist = [d.upload_time for d in data]

    for time in timelist:
        selected = data.filter(instrument=target_instrument, upload_time=time)
        if selected.exists():
            result.append(selected[0].sd)
        else:
            result.append(None)
    return result

def get_mean(data, target_instrument):

    # 获取不同仪器的mean值
    result = []
    timelist = [d.upload_time for d in data]

    for time in timelist:
        selected = data.filter(instrument=target_instrument, upload_time=time)
        if selected.exists():
            result.append(selected[0].mean)
        else:
            result.append(None)
    return result

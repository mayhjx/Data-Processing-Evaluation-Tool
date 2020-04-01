from datetime import date

from django.db import models


class QCframe(models.Model):

    # 质控框架
    # 将仪器，项目简称和质控编号，均值，标准差拆分成两个表更好 20200301
    instrument = models.CharField("仪器", max_length=10)
    item = models.CharField("项目简称", max_length = 10)
    qc_name = models.CharField("质控编号", max_length=20)
    mean = models.FloatField("均值")
    sd = models.FloatField("标准差")
    

    def __str__(self):
        return "仪器: {0} 项目简称: {1} 水平: {2}".format(
                self.instrument, self.item, self.qc_name)

    class Meta:
        verbose_name = "QC框架"
        verbose_name_plural = "QC框架"


class IonRatioFrame(models.Model):
    instrument = models.CharField("仪器", max_length=10)
    item = models.CharField("项目简称", max_length = 10)
    IonRatio = models.FloatField("Ion Ratio")

    def __str__(self):
        return "仪器: {0} 项目简称: {1}".format(
                self.instrument, self.item)

    class Meta:
        verbose_name = "Ion Ratio框架"
        verbose_name_plural = "Ion Ratio框架"



class QCrecord(models.Model):

    # 质控偏倚
    upload_time = models.DateTimeField("上传时间", auto_now_add=True)
    instrument = models.CharField("仪器", max_length=10)
    item = models.CharField("项目简称", max_length=10)
    qc_name = models.CharField("质控编号", max_length=20)
    qc_result = models.FloatField("质控偏倚")

    def __str__(self):
        return "QC Record Insutrument: {0} item: {1} {2} RSD: {3}".format(
                self.instrument, self.item, self.qc_name, self.qc_result)

    class Meta:
        verbose_name = "QC结果"
        verbose_name_plural = "QC结果"


class BigDataFrame(models.Model):

    # 不同月份对应不同均值和标准差
    Month = [('01','一月份'),
            ('02','二月份'),
            ('03','三月份'),
            ('04','四月份'),
            ('05','五月份'),
            ('06','六月份'),
            ('07','七月份'),
            ('08','八月份'),
            ('09','九月份'),
            ('10','十月份'),
            ('11','十一月份'),
            ('12','十二月份'),
            ]
    month = models.CharField('月份', choices=Month, max_length=10)
    mean = models.FloatField("均值")
    sd = models.FloatField("标准差")
    
    def __str__(self):
        return "{}月： 大数据均值{}, 标准差{}".format(self.month, self.mean, self.sd)

    class Meta:
        verbose_name = '大数据范围'
        verbose_name_plural = '大数据范围'


class PatientResult(models.Model):

    # 病人结果较大数据均值的偏倚
    upload_time = models.DateTimeField("上传时间", auto_now_add=True)
    # time = models.DateTimeField("日期", default=date.today())
    instrument = models.CharField("仪器", max_length=10)
    platenum = models.CharField("板号", max_length=4)
    num = models.IntegerField("数量")
    mean = models.FloatField("均值")
    sd = models.FloatField("ISD")

    def __str__(self):
        return "{} {}".format(self.upload_time, self.instrument)
    class Meta:
        verbose_name = '病人结果分布'
        verbose_name_plural = '病人结果分布'
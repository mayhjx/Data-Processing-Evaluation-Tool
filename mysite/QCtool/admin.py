# Register your models here.
from django.contrib import admin

from .models import BigDataFrame, PatientResult, QCframe, QCrecord, IonRatioFrame

admin.AdminSite.site_header = "质控参数设置"
admin.AdminSite.site_title = "质控系统"

# admin.site.disable_action('delete_selected')

@admin.register(QCframe)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("instrument", "qc_name", "item", "mean", "sd")
    list_filter = ('instrument', 'qc_name', 'item',)


# @admin.register(QCrecord)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = ("upload_time", "instrument", "item", "qc_name", "qc_result")
#     date_hierarchy = 'upload_time'
#     list_filter = ('instrument', 'upload_time')


@admin.register(BigDataFrame)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("month", "mean", "sd")
    list_filter = ('month',)

@admin.register(IonRatioFrame)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("instrument", "item", "IonRatio")
    list_filter = ('instrument', 'item',)


# @admin.register(PatientResult)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = ("upload_time", "instrument", "platenum", "num", "mean", "sd")
#     list_filter = ("upload_time", "instrument")

from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_upload, name='upload'),
    path('show_table_chart/', views.show_table_chart, name='show_table_chart'),
]
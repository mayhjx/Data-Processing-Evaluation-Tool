# Generated by Django 2.2.5 on 2020-03-31 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QCtool', '0010_remove_patientresult_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='IonRatioFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.CharField(max_length=10, verbose_name='仪器')),
                ('item', models.CharField(max_length=10, verbose_name='项目简称')),
                ('IonRatio', models.FloatField(verbose_name='Ion Ratio')),
            ],
            options={
                'verbose_name': 'Ion Ratio框架',
                'verbose_name_plural': 'Ion Ratio框架',
            },
        ),
        migrations.AlterField(
            model_name='patientresult',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='上传时间'),
        ),
    ]

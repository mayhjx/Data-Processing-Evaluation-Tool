# Generated by Django 2.2.5 on 2019-10-25 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QCtool', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BigDataFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(choices=[('1', '一月份'), ('2', '二月份'), ('3', '三月份'), ('4', '四月份'), ('5', '五月份'), ('6', '六月份'), ('7', '七月份'), ('8', '八月份'), ('9', '九月份'), ('10', '十月份'), ('11', '十一月份'), ('12', '十二月份')], verbose_name='月份')),
                ('mean', models.FloatField(verbose_name='均值')),
                ('sd', models.FloatField(verbose_name='标准差')),
            ],
            options={
                'verbose_name': '大数据范围',
                'verbose_name_plural': '大数据范围',
            },
        ),
        migrations.AlterField(
            model_name='qcframe',
            name='instrument',
            field=models.CharField(max_length=10, verbose_name='仪器'),
        ),
    ]

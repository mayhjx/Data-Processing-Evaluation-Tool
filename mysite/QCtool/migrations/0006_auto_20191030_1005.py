# Generated by Django 2.2.5 on 2019-10-30 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QCtool', '0005_auto_20191026_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientresult',
            name='platenum',
            field=models.CharField(max_length=4, verbose_name='板号'),
        ),
    ]
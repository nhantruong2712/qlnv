# Generated by Django 3.2.7 on 2021-09-19 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sanxuat', '0003_sanpham_congdoan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sanpham',
            name='CongDoan',
        ),
    ]
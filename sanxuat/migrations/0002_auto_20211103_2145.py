# Generated by Django 3.2.8 on 2021-11-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanxuat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chuyen',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='chuyen',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='congdoan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='congdoan',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='nhanvien',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='nhanvien',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sanpham',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sanpham',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='congdoan',
            name='ThoiGianHoanThanh',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Thời Gian Hoàn Thành'),
        ),
    ]

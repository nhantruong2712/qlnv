# Generated by Django 3.2.8 on 2021-11-30 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanxuat', '0001_initial'),
        ('QuyTrinhSanXuat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gan',
            name='NhanVien',
        ),
        migrations.AddField(
            model_name='gan',
            name='NhanVien',
            field=models.ManyToManyField(blank=True, null=True, to='sanxuat.NhanVien'),
        ),
    ]

# Generated by Django 3.2.8 on 2021-11-21 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sanxuat', '0008_auto_20211119_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhanvien',
            name='User',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhan_vien', to=settings.AUTH_USER_MODEL),
        ),
    ]

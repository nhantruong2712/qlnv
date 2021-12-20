# Generated by Django 3.2.8 on 2021-12-18 13:44

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('sanxuat', '0001_initial'),
        ('QuyTrinhSanXuat', '0001_initial'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='gan',
            name='NhanVien',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, null=True, to='sanxuat.NhanVien'),
        ),
    ]

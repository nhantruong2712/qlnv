# Generated by Django 3.2.7 on 2021-09-20 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanxuat', '0004_remove_sanpham_congdoan'),
        ('QuyTrinhSanXuat', '0002_chiacongdoan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CongDoan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanxuat.congdoan')),
                ('GanCongDoan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuyTrinhSanXuat.gancongdoan')),
            ],
        ),
        migrations.DeleteModel(
            name='ChiaCongDoan',
        ),
        migrations.CreateModel(
            name='ChiaCongDoan',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('QuyTrinhSanXuat.gancongdoan',),
        ),
        migrations.RemoveField(
            model_name='gancongdoan',
            name='CongDoan',
        ),
        migrations.AddField(
            model_name='gancongdoan',
            name='CongDoan',
            field=models.ManyToManyField(through='QuyTrinhSanXuat.Gan', to='sanxuat.CongDoan'),
        ),
    ]
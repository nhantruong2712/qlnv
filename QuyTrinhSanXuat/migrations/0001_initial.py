# Generated by Django 3.2.8 on 2021-10-30 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sanxuat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TongThoiGianCuaNhanVien', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('CongDoan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanxuat.congdoan')),
            ],
        ),
        migrations.CreateModel(
            name='GanCongDoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SaiSoChoPhep', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('TongNhanVien', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('TongThoiGian', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('NhipSanXuat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SoLuong1Ngay', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SoLuongSanPham', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SoNgayHoanThanh', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SanLuong1Gio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CongDoan', models.ManyToManyField(through='QuyTrinhSanXuat.Gan', to='sanxuat.CongDoan')),
                ('TenSanPham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanxuat.sanpham')),
            ],
            options={
                'verbose_name_plural': 'Gán Công Đoạn',
            },
        ),
        migrations.CreateModel(
            name='SoLuongLam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TongThoiGianCuaNhanVien', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('GiaCongDoan', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('LuongNgay', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SoLuongToiThieu', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('LuongNgayToiThieu', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('SoLuongDatTiepTheo', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('LuongKhiDatSoTiepTheo', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('KichCauDeTangLuong', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('GanCongDoan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyTrinhSanXuat.gancongdoan')),
                ('NhanVien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sanxuat.nhanvien')),
                ('SanPham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanxuat.sanpham')),
            ],
        ),
        migrations.AddField(
            model_name='gan',
            name='GanCongDoan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuyTrinhSanXuat.gancongdoan'),
        ),
        migrations.AddField(
            model_name='gan',
            name='NhanVien',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sanxuat.nhanvien'),
        ),
        migrations.CreateModel(
            name='ChiaCongDoan',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Chia Công Đoạn',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('QuyTrinhSanXuat.gancongdoan',),
        ),
    ]

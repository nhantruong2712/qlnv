from django.db.models.deletion import CASCADE
from sanxuat.models import SanPham
from django.db import models
from sanxuat.models import *
from django.urls import reverse


class GanCongDoan(models.Model):
    TenSanPham = models.ForeignKey(SanPham, on_delete=CASCADE)
    CongDoan = models.ManyToManyField(CongDoan, through='Gan')
    SaiSoChoPhep = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TongNhanVien = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    TongThoiGian = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    NhipSanXuat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuong1Ngay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuongSanPham = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoNgayHoanThanh = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SanLuong1Gio = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def get_absolute_url(self):
        return reverse("quytrinhsanxuat:tao-san-pham")

    def __str__(self):
        return str(self.TenSanPham) + " " + str(self.CongDoan)


class ChiaCongDoan(GanCongDoan):
    class Meta:
        proxy = True

    def __str__(self):
        return f"Chia cong doan {self.TenSanPham}"

    def save(self, *args, **kwargs):
        return None

    # @property
    # def Thoigian(self):
    #     return self.CongDoan.ThoiGianHoanThanh


class Gan(models.Model):

    CongDoan = models.ForeignKey(CongDoan, on_delete=models.CASCADE)
    GanCongDoan = models.ForeignKey(GanCongDoan, on_delete=models.CASCADE)
    NhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, null=True, blank=True)
    TongThoiGianCuaNhanVien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Before update value
        obj = Gan.objects.values('NhanVien', 'TongThoiGianCuaNhanVien').get(pk=self.pk)
        if obj['NhanVien'] is not None:
            gans = Gan.objects.filter(NhanVien__id=obj['NhanVien'], GanCongDoan__id=self.GanCongDoan.id)
            if gans.count() == 0:
                self.TongThoiGianCuaNhanVien = None
            elif gans.count() == 1:
                self.TongThoiGianCuaNhanVien = self.CongDoan.ThoiGianHoanThanh
            else:
                total_time = gans[0].TongThoiGianCuaNhanVien
                total_time -= self.CongDoan.ThoiGianHoanThanh
                self.TongThoiGianCuaNhanVien = total_time
                gans.update(TongThoiGianCuaNhanVien=total_time)
        else:
            self.TongThoiGianCuaNhanVien = None
        # After update value
        if self.NhanVien is None:
            self.TongThoiGianCuaNhanVien = None
        else:
            gans = Gan.objects.filter(NhanVien__id=self.NhanVien.id, GanCongDoan__id=self.GanCongDoan.id)
            if gans.count() == 0:
                self.TongThoiGianCuaNhanVien = self.CongDoan.ThoiGianHoanThanh
            else:
                total_time = gans[0].TongThoiGianCuaNhanVien
                total_time += self.CongDoan.ThoiGianHoanThanh
                self.TongThoiGianCuaNhanVien = total_time
                gans.update(TongThoiGianCuaNhanVien=total_time)

        return super(Gan, self).save(*args, **kwargs)


class SoLuongLam(models.Model):
    NhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, null=True, blank=True)
    SanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    GanCongDoan = models.ForeignKey(GanCongDoan, on_delete=models.CASCADE, null=True)
    TongThoiGianCuaNhanVien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    GiaCongDoan = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    LuongNgay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuongToiThieu = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    LuongNgayToiThieu = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuongDatTiepTheo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    KichCauDeTangLuong = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.SanPham.TenSanPham


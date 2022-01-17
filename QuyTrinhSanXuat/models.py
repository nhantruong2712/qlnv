from sanxuat.models import SanPham
from sanxuat.models import *
# from sortedm2m.fields import SortedManyToManyField


class GanCongDoan(models.Model):
    TenSanPham = models.ForeignKey(SanPham, on_delete=CASCADE, limit_choices_to={'hoan_tat': False})
    CongDoan = models.ManyToManyField(CongDoan, through='Gan')
    SaiSoChoPhep = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TongNhanVien = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    TongThoiGian = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    NhipSanXuat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuong1Ngay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoLuongSanPham = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SoNgayHoanThanh = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    SanLuong1Gio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = 'Gán Công Đoạn'

    def __str__(self):
        return str(self.TenSanPham)

    def delete(self, *args, **kwargs):
        SoLuongMoiGio.objects.filter(SanPham=self.TenSanPham).delete()
        return super(GanCongDoan, self).delete(*args, **kwargs)


class ChiaCongDoan(GanCongDoan):
    class Meta:
        proxy = True
        verbose_name_plural = 'Chia Công Đoạn'

    def __str__(self):
        return f"Chia cong doan {self.TenSanPham} - {self.created_at.date()}"

    def save(self, *args, **kwargs):
        return None


class Gan(models.Model):
    CongDoan = models.ForeignKey(CongDoan, on_delete=models.CASCADE)
    GanCongDoan = models.ForeignKey(GanCongDoan, on_delete=models.CASCADE)
    NhanVien = models.ManyToManyField(NhanVien, null=True, blank=True)
    TongThoiGianCuaNhanVien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = 'Gán'

    # def __str__(self):
    #     return "{} - {}".format(self.GanCongDoan.TenSanPham.TenSanPham, self.CongDoan.TenCongDoan)

    def save_without_do_something(self, *args, **kwargs):
        return super(Gan, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Before update value
    #     try:
    #         a = self.NhanVien.all()
    #         obj = Gan.objects.values('NhanVien', 'TongThoiGianCuaNhanVien').get(pk=self.pk)
    #         if obj['NhanVien'] is not None:
    #             gans = Gan.objects.filter(NhanVien__id=obj['NhanVien'], GanCongDoan__id=self.GanCongDoan.id)
    #             if gans.count() == 0:
    #                 self.TongThoiGianCuaNhanVien = None
    #             elif gans.count() == 1:
    #                 self.TongThoiGianCuaNhanVien = self.CongDoan.ThoiGianHoanThanh
    #             else:
    #                 total_time = gans[0].TongThoiGianCuaNhanVien
    #                 total_time -= self.CongDoan.ThoiGianHoanThanh
    #                 self.TongThoiGianCuaNhanVien = total_time
    #                 gans.update(TongThoiGianCuaNhanVien=total_time)
    #         else:
    #             self.TongThoiGianCuaNhanVien = None
    #         # After update value
    #         if self.NhanVien is None:
    #             self.TongThoiGianCuaNhanVien = None
    #         else:
    #             gans = Gan.objects.filter(NhanVien__id=self.NhanVien.id, GanCongDoan__id=self.GanCongDoan.id)
    #             if gans.count() == 0:
    #                 self.TongThoiGianCuaNhanVien = self.CongDoan.ThoiGianHoanThanh
    #             else:
    #                 total_time = gans[0].TongThoiGianCuaNhanVien
    #                 total_time += self.CongDoan.ThoiGianHoanThanh
    #                 self.TongThoiGianCuaNhanVien = total_time
    #                 gans.update(TongThoiGianCuaNhanVien=total_time)
    #     except:
    #         pass
    #
    #     return super(Gan, self).save(*args, **kwargs)


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
    LuongKhiDatSoTiepTheo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    KichCauDeTangLuong = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return "{} - {}".format(self.SanPham.TenSanPham, self.NhanVien.TenNhanVien)


class LuongNgayNhanVien(models.Model):
    NhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    LuongNgayHomTruoc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    LuongNgayHomNay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    LuongThang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = 'Lương Ngày Của Nhân Viên'

    def __str__(self):
        return "{} - {}".format(self.NhanVien.Ho + ' ' + self.NhanVien.Ten, self.created_at.date())


class SoLuongMoiGio(models.Model):
    NhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, null=True, blank=True)
    SanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    CongDoan = models.ForeignKey(CongDoan, on_delete=models.CASCADE, null=True, blank=True)
    TamDenChinGio = models.PositiveIntegerField(null=True, blank=True, default=0)
    ChinDenMuoiGio = models.PositiveIntegerField(null=True, blank=True, default=0)
    MuoiDenMuoiMot = models.PositiveIntegerField(null=True, blank=True, default=0)
    MuoiMotDenMuoiHai = models.PositiveIntegerField(null=True, blank=True, default=0)
    MotDenHai = models.PositiveIntegerField(null=True, blank=True, default=0)
    HaiDenBa = models.PositiveIntegerField(null=True, blank=True, default=0)
    BaDenBon = models.PositiveIntegerField(null=True, blank=True, default=0)
    BonDenNam = models.PositiveIntegerField(null=True, blank=True, default=0)
    ThemGio = models.PositiveIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = 'Số Lượng Làm Mỗi Giờ'

    def __str__(self):
        return "{} - {} - {} - {}".format(self.SanPham.TenSanPham, self.NhanVien.Ho + ' ' + self.NhanVien.Ten, self.CongDoan.TenCongDoan,
                                          self.created_at.date())

    def save(self, *args, **kwargs):
        try:
            luong_ngay = LuongNgayNhanVien.objects.get(NhanVien=self.NhanVien, created_at__date=self.created_at.date())

            tong_so_luong = (self.TamDenChinGio + self.ChinDenMuoiGio + self.MuoiDenMuoiMot +
                             self.MotDenHai + self.HaiDenBa + self.BaDenBon + self.BonDenNam + self.ThemGio)
            luong_ngay.LuongNgayHomNay = self.CongDoan.DonGia * tong_so_luong
            luong_ngay.save()
            luong_thang = LuongNgayNhanVien.objects.filter(NhanVien=self.NhanVien,
                                                           created_at__month=self.created_at.month,
                                                           created_at__year=self.created_at.year)
            tong_luong_ngay = 0
            for luong in luong_thang:
                tong_luong_ngay += luong.LuongNgayHomNay
            for luong in luong_thang:
                luong.LuongThang = tong_luong_ngay
                luong.save()
        except:
            pass
        return super(SoLuongMoiGio, self).save(*args, **kwargs)

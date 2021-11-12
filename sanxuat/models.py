from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from cauhinh.models import thietbi, bactho, chucvu


class CongDoan(models.Model):
    class Meta:
        verbose_name_plural = 'Công Đoạn'
    NHOMCONGDOAN_CHOICES = (
        ('CB','CHUẨN BỊ'),
        ('SX','SẢN XUẤT'),
        ('HT','HOÀN THÀNH'),
    )
    TenCongDoan = models.TextField(verbose_name='Tên Công Đoạn')
    NhomCongDoan = models.CharField(max_length=2, choices=NHOMCONGDOAN_CHOICES, default=2, verbose_name='Nhóm Công Đoạn')
    ThoiGianHoanThanh = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Thời Gian Hoàn Thành',
                                            null=True, blank=True)
    ThietBi = models.ForeignKey(thietbi, on_delete=CASCADE, verbose_name='Thiết Bị')
    BacTho = models.ForeignKey(bactho, on_delete=CASCADE, verbose_name='Bậc Thợ')
    DonGia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Đơn Giá')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        x = bactho.objects.get(tenbactho=self.BacTho) #lấy từ trong bảng bactho để lấy giá trị tương ứng với name
        self.DonGia = self.ThoiGianHoanThanh * x.dongia
        return super(CongDoan, self).save(*args, **kwargs)

    def __str__(self):
        return self.TenCongDoan


class Chuyen(models.Model):
    class Meta:
        verbose_name_plural = 'Chuyền'
    TenChuyen = models.TextField(verbose_name='Tên Chuyền')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.TenChuyen


class NhanVien(models.Model):
    class Meta:
        verbose_name_plural = 'Nhân Viên'
    TINHTRANG_CHOICES = (
        ('BT','BÌNH THƯỜNG'),
        ('TN','TẠM NGHỈ'),
        ('NV','NGHỈ VIỆC'),
    )
    User = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    TenNhanVien = models.CharField(max_length=255, verbose_name='Tên Nhân Viên', null=True)
    BacTho = models.ForeignKey(bactho, on_delete=CASCADE, verbose_name='Bậc Thợ', null = True, blank=True)
    SoDienThoai = models.IntegerField(verbose_name='Số Điện Thoại', null = True, blank=True)
    NgaySinh = models.DateField(verbose_name='Ngày Sinh', null = True, blank=True)
    DiaChi = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Đại Chỉ', null=True)
    ChucDanh = models.ForeignKey(chucvu, on_delete=CASCADE, verbose_name='Chức Danh', null = True, blank=True)
    MayUT1 = models.ForeignKey(thietbi, on_delete=CASCADE, verbose_name='Ưu Tiên 1', null = True, blank=True)
    TenChuyen = models.ForeignKey(Chuyen, on_delete=CASCADE, verbose_name='Thuộc Chuyền', null = True, blank=True)
    TinhTrang = models.CharField(max_length=20, choices=TINHTRANG_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.TenNhanVien if self.TenNhanVien else self.User.username


class SanPham(models.Model):
    class Meta:
        verbose_name_plural = 'Sản Phẩm'
    MaSanPham = models.TextField(verbose_name='Mã Sản Phẩm')
    TenSanPham = models.TextField(verbose_name='Tên Sản Phẩm')
    SoLuong = models.IntegerField(verbose_name='Số Lượng')
    DonGia = models.FloatField(verbose_name='Đơn Giá')
    NgayDongBo = models.DateField(verbose_name='Ngày Đồng Bộ')
    NgayGiaoHang = models.DateField(verbose_name='Ngày Giao Hàng')
    ChuyenThucHien = models.ForeignKey(Chuyen, on_delete=CASCADE, verbose_name='Giao Việc Cho')
    DienGiai = models.TextField(verbose_name='Ghi Chú')
    hoan_tat = models.BooleanField(default=False, verbose_name='Hoàn tất')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # CongDoan = models.ManyToManyField(CongDoan)

    def __str__(self):
        return self.MaSanPham

# class Product(models.Model):
#    name = models.CharField(max_length=255)
#    price = models.DecimalField(max_digits=10, decimal_places=2)
#    inventory = models.IntegerField(default=0)
#    price_total = models.DecimalField(max_digits=10, decimal_places=2,null = True, blank= True)
#    def save(self, *args, **kwargs):
#        self.price_total = self.price * self.inventory
#        return super(Product, self).save(*args, **kwargs)
#    def __str__(self):
#        return self.name

# class ViDuDropDown(models.Model):
#    NHOMCONGDOAN_CHOICES = (
#        (1,'CHUẨN BỊ'),
#        (2,'SẢN XUẤT'),
#        (3,'HOÀN THÀNH'),
#    )
#    giatridropdown = models.CharField(max_length=1, choices = NHOMCONGDOAN_CHOICES)
    

# Create your models here.

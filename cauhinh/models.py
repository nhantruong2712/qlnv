from django.db import models
from django.db import connections
from django.db.models.expressions import Value
from django.db.models.fields import TextField
#from .xuly import tinhtoan

#from cauhinh.models import phongban



class bactho(models.Model):
    tenbactho = models.TextField(verbose_name='Tên Bậc Thợ')
    dongia = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Đơn Giá')
    LuongTamTinh = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Lương Tạm Tính')
    class Meta:
        verbose_name_plural = 'Bậc Thợ'
    def __str__(self):
        return self.tenbactho


class phongban(models.Model):
    tenphongban = models.TextField(verbose_name='Tên Phòng Ban')
    diengiai = models.TextField(verbose_name='Diễn Giải')
    class Meta:
        verbose_name_plural = 'Phòng Ban'

    def __str__(self):
        return self.tenphongban

class chucvu(models.Model):
    tenchucvu = models.TextField(verbose_name='Tên Chức Vụ')
    tenphongban = models.ForeignKey(phongban, on_delete=models.CASCADE,verbose_name='Tên Phòng Ban')
    class Meta:
        verbose_name_plural = 'Chức Vụ'
    
    def __str__(self):
        return self.tenchucvu
    

class thietbi(models.Model):
    tenthietbi = models.TextField(verbose_name='Tên Thiết Bị')
    soluong = models.IntegerField(verbose_name='Số Lượng')
    class Meta:
        verbose_name_plural = 'Thiết Bị'
    def __str__(self):
        return self.tenthietbi

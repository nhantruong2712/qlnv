from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from sanxuat.models import CongDoan

from .models import ChiaCongDoan, GanCongDoan, Gan, SoLuongLam
# Register your models here.

    
class GanCongDoanForm(forms.ModelForm):
    CongDoan = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple('Công đoạn', False),
            queryset = CongDoan.objects.all())


class GanCongDoanAdmin(admin.ModelAdmin):
    form = GanCongDoanForm
    exclude = ['TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SoLuong1Ngay', 'SoLuongSanPham', 'SoNgayHoanThanh',
               'SanLuong1Gio', 'SoLuongLam']


class ChiaCongDoanInline(admin.TabularInline):
    model = Gan
    extra = 0
    fields = ['CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'NhanVien', 'TongThoiGian', 'Bac', 'May']
    readonly_fields = ('CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'TongThoiGian', 'Bac', 'May')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def ThoiGian(self, instance):
        return instance.CongDoan.ThoiGianHoanThanh

    def ThietBi(self, instance):
        return instance.CongDoan.ThietBi

    def BacTho(self, instance):
        return instance.CongDoan.BacTho

    def Bac(self, instance):
        return instance.NhanVien.BacTho

    def May(self, instance):
        return instance.NhanVien.MayUT1

    def TongThoiGian(self, instance):
        return instance.TongThoiGianCuaNhanVien

class NhanVienInline(admin.TabularInline):
    model = SoLuongLam
    extra = 0
    fields = ['NhanVien', 'TongThoiGianCuaNhanVien', 'GiaCongDoan', 'LuongNgay', 'SoLuongToiThieu', 'LuongNgayToiThieu',
              'SoLuongDatTiepTheo', 'KichCauDeTangLuong']
    # readonly_fields = ('CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'TongThoiGian', 'Bac', 'May')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def NhanVien(self, instance):
        return instance.NhanVien

    def TongThoiGianCuaNhanVien(self, instance):
        return instance.TongThoiGianCuaNhanVien

    def GiaCongDoan(self, instance):
        return instance.GiaCongDoan

    def LuongNgay(self, instance):
        return instance.CongDoan.ThietBi

    def SoLuongToiThieu(self, instance):
        return instance.CongDoan.BacTho

    def LuongNgayToiThieu(self, instance):
        return instance.NhanVien.BacTho

    def SoLuongDatTiepTheo(self, instance):
        return instance.NhanVien.MayUT1

    def KichCauDeTangLuong(self, instance):
        return instance.NhanVien.MayUT1


class ChiaCongDoanAdmin(admin.ModelAdmin):
    inlines = [ChiaCongDoanInline, NhanVienInline]
    readonly_fields = ('TenSanPham', 'TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SaiSoChoPhep', 'SoLuong1Ngay',
                       'SoLuongSanPham', 'SoNgayHoanThanh', 'SanLuong1Gio')

    # change_form_template = "gan_changeform.html"


class SoLuongLamAdmin(admin.ModelAdmin):
    inlines = [NhanVienInline]
    # readonly_fields = ('NhanVien', 'TongThoiGian', 'GiaCongDoan', 'LuongNgay', 'SoLuongToiThieu', 'LuongNgayToiThieu',
    #                     'SoLuongDatTiepTheo', 'KichCauDeTangLuong')


admin.site.register(GanCongDoan, GanCongDoanAdmin)
admin.site.register(ChiaCongDoan, ChiaCongDoanAdmin)
# admin.site.register(SoLuongLam, SanPhamAdmin)

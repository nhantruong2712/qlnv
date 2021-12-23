from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from sanxuat.models import CongDoan, NhanVien
from .models import ChiaCongDoan, GanCongDoan, Gan, SoLuongLam, SoLuongMoiGio, LuongNgayNhanVien


class GanCongDoanForm(forms.ModelForm):
    CongDoan = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple('Công đoạn', False),
                                              queryset=CongDoan.objects.all())


class GanCongDoanAdmin(admin.ModelAdmin):
    form = GanCongDoanForm
    exclude = ['TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SoLuong1Ngay', 'SoLuongSanPham', 'SoNgayHoanThanh',
               'SanLuong1Gio', 'SoLuongLam']


class ChiaCongDoanInline(admin.TabularInline):
    model = Gan
    extra = 0
    fields = ['CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'NhanVien', 'Bac', 'May'] # 'TongThoiGian',
    readonly_fields = ('CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'Bac', 'May') # 'TongThoiGian',
    ordering = ["CongDoan", "NhanVien"]
    filter_horizontal = ('NhanVien', )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        nhan_vien_field = super(ChiaCongDoanInline, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'NhanVien':
            gan = self.model.objects.first()
            try:
                nhan_vien_field.queryset = nhan_vien_field.queryset.filter(TenChuyen=gan.GanCongDoan.TenSanPham.ChuyenThucHien)
            except:
                print("No DataBase to filter")
                pass
        return nhan_vien_field

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
        try:
            return instance.NhanVien.all()[0].BacTho
        except:
            return None

    def May(self, instance):
        try:
            return instance.NhanVien.all()[0].MayUT1
        except:
            return None

    # def TongThoiGian(self, instance):
    #     if instance.NhanVien.all().count() == 1:
    #         so_luong_lam = SoLuongLam.objects.get(NhanVien=instance.NhanVien.all()[0],
    #                                               SanPham=instance.GanCongDoan.TenSanPham)
    #         return so_luong_lam.TongThoiGianCuaNhanVien
    #     return None


class NhanVienInline(admin.TabularInline):
    model = SoLuongLam
    extra = 0
    fields = ['NhanVien', 'TongThoiGianCuaNhanVien', 'GiaCongDoan', 'LuongNgay', 'SoLuongToiThieu', 'LuongNgayToiThieu',
              'SoLuongDatTiepTheo', 'LuongKhiDatSoTiepTheo', 'KichCauDeTangLuong']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class ChiaCongDoanAdmin(admin.ModelAdmin):
    inlines = [NhanVienInline, ChiaCongDoanInline]
    readonly_fields = ('TenSanPham', 'TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SaiSoChoPhep', 'SoLuong1Ngay',
                       'SoLuongSanPham', 'SoNgayHoanThanh', 'SanLuong1Gio')

    change_form_template = "gan_changeform.html"


class SoLuongLamAdmin(admin.ModelAdmin):
    inlines = [NhanVienInline]


admin.site.register(SoLuongLam)
admin.site.register(GanCongDoan, GanCongDoanAdmin)
admin.site.register(ChiaCongDoan, ChiaCongDoanAdmin)
admin.site.register(SoLuongMoiGio)
admin.site.register(LuongNgayNhanVien)
admin.site.register(Gan)

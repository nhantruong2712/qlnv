import tablib
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sanxuat.models import CongDoan
from .func import thousand_format
from .models import ChiaCongDoan, GanCongDoan, Gan, SoLuongLam, SoLuongMoiGio, LuongNgayNhanVien


class GanCongDoanForm(forms.ModelForm):
    CongDoan = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple('Công đoạn', False),
                                              queryset=CongDoan.objects.all())


class GanCongDoanAdmin(admin.ModelAdmin):
    form = GanCongDoanForm
    exclude = ['TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SoLuong1Ngay', 'SoLuongSanPham', 'SoNgayHoanThanh',
               'SanLuong1Gio', 'SoLuongLam']


class ChiaCongDoanResource(resources.ModelResource):
    class Meta:
        model = ChiaCongDoan


class SoLuongLamResource(resources.ModelResource):
    class Meta:
        model = SoLuongLam

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()
        ds = tablib.Dataset()
        data = []
        for chia_cong_doan in queryset:
            for so_luong_lam in chia_cong_doan.soluonglam_set.all():
                row = {
                    'Nhan Vien': so_luong_lam.NhanVien.Ho + ' ' + so_luong_lam.NhanVien.Ten,
                    'Tong Thoi Gian': so_luong_lam.TongThoiGianCuaNhanVien,
                    'Gia Cong Doan': so_luong_lam.GiaCongDoan,
                    'Luong Ngay': thousand_format(so_luong_lam.LuongNgay),
                    'So Luong Toi Thieu': thousand_format(so_luong_lam.SoLuongToiThieu),
                    'Luong Ngay Toi Thieu': thousand_format(so_luong_lam.LuongNgayToiThieu),
                    'So Luong Dat Tiep Theo': thousand_format(so_luong_lam.SoLuongDatTiepTheo),
                    'Luong Dat Tiep Theo': thousand_format(so_luong_lam.LuongKhiDatSoTiepTheo),
                    'Kich Cau Tang Luong': thousand_format(so_luong_lam.KichCauDeTangLuong),
                }
                data.append(row)
        ds.dict = data
        return ds


class ChiaCongDoanInline(admin.TabularInline):
    model = Gan
    extra = 0
    fields = ['CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'NhanVien', 'Bac', 'May']  # 'TongThoiGian',
    readonly_fields = ('CongDoan', 'BacTho', 'ThoiGian', 'ThietBi', 'Bac', 'May')  # 'TongThoiGian',
    ordering = ["CongDoan", "NhanVien"]
    filter_horizontal = ('NhanVien',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        nhan_vien_field = super(ChiaCongDoanInline, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'NhanVien':
            gan = self.model.objects.first()
            try:
                nhan_vien_field.queryset = nhan_vien_field.queryset.filter(
                    TenChuyen=gan.GanCongDoan.TenSanPham.ChuyenThucHien)
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
    ordering = ["NhanVien__Ten"]
    fields = ['NhanVien', 'tong_thoi_gian', 'GiaCongDoan', 'luong_ngay', 'so_luong_toi_thieu', 'luong_ngay_toi_thieu',
              'so_luong_dat_tiep_theo', 'luong_dat_tiep_theo', 'kich_cau_tang_luong']
    readonly_fields = (
        'NhanVien', 'tong_thoi_gian', 'GiaCongDoan', 'luong_ngay', 'so_luong_toi_thieu', 'luong_ngay_toi_thieu',
        'so_luong_dat_tiep_theo', 'luong_dat_tiep_theo', 'kich_cau_tang_luong')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def tong_thoi_gian(self, instance):
        return thousand_format(instance.TongThoiGianCuaNhanVien)

    def luong_ngay(self, instance):
        return thousand_format(instance.LuongNgay)

    def so_luong_toi_thieu(self, instance):
        return thousand_format(instance.SoLuongToiThieu)

    def luong_ngay_toi_thieu(self, instance):
        return thousand_format(instance.LuongNgayToiThieu)

    def so_luong_dat_tiep_theo(self, instance):
        return thousand_format(instance.SoLuongDatTiepTheo)

    def luong_dat_tiep_theo(self, instance):
        return thousand_format(instance.LuongKhiDatSoTiepTheo)

    def kich_cau_tang_luong(self, instance):
        return thousand_format(instance.KichCauDeTangLuong)


class ChiaCongDoanAdmin(ImportExportModelAdmin):
    inlines = [NhanVienInline, ChiaCongDoanInline]
    resource_class = SoLuongLamResource
    readonly_fields = ('TenSanPham', 'TongNhanVien', 'TongThoiGian', 'NhipSanXuat', 'SaiSoChoPhep', 'SoLuong1Ngay',
                       'SoLuongSanPham', 'SoNgayHoanThanh', 'SanLuong1Gio')

    change_form_template = "gan_changeform.html"


class SoLuongLamAdmin(admin.ModelAdmin):
    list_display = (
        'NhanVien', 'SanPham', 'GanCongDoan', 'tong_thoi_gian', 'gia_cong_doan', 'luong_ngay', 'so_luong_toi_thieu',
        'luong_ngay_toi_thieu', 'so_luong_dat_tiep_theo', 'luong_dat_tiep_theo',)

    def tong_thoi_gian(self, instance):
        return thousand_format(instance.TongThoiGianCuaNhanVien)

    def gia_cong_doan(self, instance):
        return thousand_format(instance.GiaCongDoan)

    def so_luong_toi_thieu(self, instance):
        return thousand_format(instance.SoLuongToiThieu)

    def luong_ngay_toi_thieu(self, instance):
        return thousand_format(instance.LuongNgayToiThieu)

    def so_luong_dat_tiep_theo(self, instance):
        return thousand_format(instance.SoLuongDatTiepTheo)

    def luong_dat_tiep_theo(self, instance):
        return thousand_format(instance.LuongKhiDatSoTiepTheo)

    def luong_ngay(self, instance):
        return thousand_format(instance.LuongNgay)


class SoLuongLamMoiGioAdmin(admin.ModelAdmin):
    list_display = (
        'NhanVien', 'SanPham', 'CongDoan', 'TamDenChinGio', 'ChinDenMuoiGio', 'MuoiDenMuoiMot', 'MuoiMotDenMuoiHai',
        'MotDenHai', 'HaiDenBa', 'BaDenBon', 'BonDenNam', 'ThemGio',)


admin.site.register(SoLuongLam, SoLuongLamAdmin)
admin.site.register(GanCongDoan, GanCongDoanAdmin)
admin.site.register(ChiaCongDoan, ChiaCongDoanAdmin)
admin.site.register(SoLuongMoiGio, SoLuongLamMoiGioAdmin)
admin.site.register(LuongNgayNhanVien)
admin.site.register(Gan)

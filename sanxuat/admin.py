from django.contrib import admin
from django.contrib.admin.decorators import display
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


class NhanVienResource(resources.ModelResource):
    class Meta:
        model = NhanVien


class CongDoanResource(resources.ModelResource):
    class Meta:
        model = CongDoan


class NhanVienAdmin(ImportExportModelAdmin):
    resource_class = NhanVienResource
    list_filter = ('TenChuyen',)
    search_fields = ['Ho', 'Ten']


class CongDoanAdmin(ImportExportModelAdmin):
    resource_class = CongDoanResource


admin.site.register(SanPham)
admin.site.register(CongDoan, CongDoanAdmin)
admin.site.register(Chuyen)
admin.site.register(NhanVien, NhanVienAdmin)
# Register your models here.

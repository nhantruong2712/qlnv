from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from datetime import date, timedelta
from django.contrib.auth.models import User

from . import constants
from .models import GanCongDoan, CongDoan, Gan, ChiaCongDoan, SoLuongLam, SoLuongMoiGio, LuongNgayNhanVien
from .utils import AssignTask
from sanxuat.models import NhanVien, SanPham
from decimal import Decimal
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=GanCongDoan.CongDoan.through)
def gancongdoan_congdoan_changed(sender, instance, action, **kwargs):
    actions = ["post_add", "post_remove", "post_clear"]
    if action in actions:
        assign_task = AssignTask()
        assign_task.get_tolerance(instance.SaiSoChoPhep)
        assign_task.get_conveyor(instance.TenSanPham.ChuyenThucHien)
        assign_task.get_conveyor_object()
        assign_task.get_emps()

        assign_task.manage.sort_list_employee_by_level()

        instance.TongNhanVien = assign_task.count_emp_in_conveyor()
        assign_task.get_id_instance(instance.id)
        assign_task.get_stages()

        instance.TongThoiGian = assign_task.get_total_time()
        instance.NhipSanXuat = assign_task.get_takl_time()
        instance.SoLuong1Ngay = assign_task.get_amount_a_day()
        instance.SoLuongSanPham = instance.TenSanPham.SoLuong
        instance.SoNgayHoanThanh = instance.SoLuongSanPham / instance.SoLuong1Ngay
        instance.SanLuong1Gio = instance.SoLuong1Ngay / 8
        instance.save()
        assign_task.divide_task()
        gan = instance.gan_set.all().values('NhanVien', 'TongThoiGianCuaNhanVien', 'CongDoan').distinct()
        for nhanvien in gan:
            if nhanvien.get('NhanVien') is None:
                pass
            else:
                congdoan = CongDoan.objects.get(id=nhanvien.get('CongDoan'))
                nhanvien_id = int(nhanvien.get('NhanVien'))
                nhanvien_obj = NhanVien.objects.get(id=nhanvien_id)
                san_pham_obj = SanPham.objects.get(id=instance.TenSanPham_id)
                # Tạo số lượng mỗi giờ
                SoLuongMoiGio.objects.create(NhanVien_id=nhanvien_id, CongDoan=congdoan, SanPham=san_pham_obj)
                if LuongNgayNhanVien.objects.filter(NhanVien_id=nhanvien_id, created_at__date=date.today()).exists():
                    pass
                else:
                    try:
                        ngay_hom_qua = date.today() - timedelta(1)
                        luong_hom_qua = LuongNgayNhanVien.objects.get(NhanVien_id=nhanvien_id, created_at=ngay_hom_qua)
                        LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id, LuongNgayHomTruoc=luong_hom_qua.LuongNgayHomTruoc)
                    except:
                        LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id)
                    if SoLuongLam.objects.filter(NhanVien=nhanvien_id, SanPham=instance.TenSanPham_id).exists():
                        nhanvienlam = SoLuongLam.objects.get(NhanVien=nhanvien_id, SanPham=instance.TenSanPham_id)
                        nhanvienlam.GiaCongDoan += congdoan.DonGia
                        nhanvienlam.LuongNgay = nhanvienlam.GiaCongDoan * instance.SoLuong1Ngay
                        nhanvienlam.LuongNgayToiThieu = nhanvienlam.SoLuongToiThieu * nhanvienlam.GiaCongDoan
                        nhanvienlam.save()
                    else:
                        SoLuongToiThieu = round(8*60*60/nhanvien.get('TongThoiGianCuaNhanVien'))
                        SoLuongDatTiepTheo = SoLuongToiThieu*(20/100)+SoLuongToiThieu
                        GiaCongDoan = congdoan.DonGia
                        SoLuongLam.objects.create(NhanVien=nhanvien_obj, SanPham=san_pham_obj, GanCongDoan=instance,
                                                  TongThoiGianCuaNhanVien=nhanvien.get('TongThoiGianCuaNhanVien'),
                                                  GiaCongDoan= GiaCongDoan, LuongNgay=GiaCongDoan*instance.SoLuong1Ngay,
                                                  SoLuongToiThieu=SoLuongToiThieu,
                                                  LuongNgayToiThieu=SoLuongToiThieu*GiaCongDoan,
                                                  SoLuongDatTiepTheo=SoLuongDatTiepTheo,
                                                  LuongKhiDatSoTiepTheo=GiaCongDoan*Decimal(SoLuongDatTiepTheo)*constants.PhanTramThuong,
                                                  KichCauDeTangLuong=SoLuongDatTiepTheo-SoLuongToiThieu)


@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    if created:
        NhanVien.objects.create(User=instance)


@receiver(post_save, sender=User)
def save_staff(sender, instance, **kwargs):
    if instance.first_name and instance.last_name:
        nhanvien = NhanVien.objects.get(User=instance)
        nhanvien.TenNhanVien = instance.first_name + ' ' + instance.last_name
        nhanvien.save()


@receiver(post_save, sender=NhanVien)
def save_staff(sender, instance, created ,**kwargs):
    if created:
        a = 'a'
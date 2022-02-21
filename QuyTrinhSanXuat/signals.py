from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from datetime import date, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from decimal import Decimal

from .models import GanCongDoan, Gan, SoLuongLam, SoLuongMoiGio, LuongNgayNhanVien
from .utils import AssignTask
from sanxuat.models import NhanVien
from cauhinh.models import CauHinhChung

# cau_hinh = CauHinhChung.objects.get(id=1)


@receiver(post_save, sender=SoLuongLam)
def tao_so_luong_lam(sender, instance, created, **kwargs):
    if created:
        gancongdoan = GanCongDoan.objects.get(TenSanPham=instance.SanPham)
        GiaCongDoan = instance.GiaCongDoan
        TongThoiGianCuaNhanVien = instance.TongThoiGianCuaNhanVien
        instance.TongThoiGianCuaNhanVien = TongThoiGianCuaNhanVien
        instance.GiaCongDoan = GiaCongDoan
        instance.LuongNgay = GiaCongDoan * gancongdoan.SoLuong1Ngay
        instance.SoLuongToiThieu = round(8 * 60 * 60 / TongThoiGianCuaNhanVien)
        instance.SoLuongDatTiepTheo = instance.SoLuongToiThieu * Decimal(20 / 100) + instance.SoLuongToiThieu
        instance.LuongNgayToiThieu = instance.SoLuongToiThieu * GiaCongDoan
        instance.LuongKhiDatSoTiepTheo = GiaCongDoan * Decimal(instance.SoLuongDatTiepTheo)
        instance.GanCongDoan = gancongdoan
        instance.KichCauDeTangLuong = instance.SoLuongDatTiepTheo - instance.SoLuongToiThieu
        instance.save()
        # create Luong Ngay Nhan Vien


@receiver(m2m_changed, sender=Gan.NhanVien.through)
def chiacongdoan_changed(sender, instance, action, **kwargs):
    change_actions = ['pre_add', 'pre_remove']
    if action in change_actions:
        instance_nhanvien = instance.NhanVien.all()
        for nhanvien in instance_nhanvien:
            # Get gán trước đó
            try:
                gans = Gan.objects.filter(NhanVien=nhanvien.id, GanCongDoan=instance.GanCongDoan)
            except:
                gans = None
            # Chưa gán nhân viên
            if gans is None:
                update = update_so_luong_lam(gan_obj=instance, nhanvien_id=nhanvien.id, cong_them=True)
                if not update:
                    SoLuongLam.objects.create(NhanVien_id=nhanvien.id,
                                              GiaCongDoan=instance.CongDoan.DonGia,
                                              TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                                              SanPham_id=instance.GanCongDoan.TenSanPham_id)
                    tao_so_luong_moi_gio(nhanvien.id, instance.CongDoan.id, instance.GanCongDoan.TenSanPham_id)
            # Đổi nhân viên thành None
            if action == 'pre_remove':
                so_luong_lam = SoLuongLam.objects.get(NhanVien_id=nhanvien.id,
                                                      SanPham=instance.GanCongDoan.TenSanPham)
                if gans.count() > 1:
                    update_so_luong_lam(gan_obj=instance, nhanvien_id=nhanvien.id, cong_them=False)
                else:
                    so_luong_lam.delete()

    actions = ["post_remove", "post_clear", "post_save", "post_add"]
    if action in actions:
        with transaction.atomic():
            try:
                instance_nhanvien = instance.NhanVien.all()
                # Đổi từ None sang nhân viên (thêm nhân viên)
                for nhanvien in instance_nhanvien:
                    update = update_so_luong_lam(gan_obj=instance, nhanvien_id=nhanvien.id, cong_them=True)
                    if not update:
                        SoLuongLam.objects.create(NhanVien_id=nhanvien.id,
                                                  GiaCongDoan=instance.CongDoan.DonGia,
                                                  TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                                                  SanPham_id=instance.GanCongDoan.TenSanPham_id)
                        tao_so_luong_moi_gio(nhanvien.id, instance.CongDoan.id, instance.GanCongDoan.TenSanPham_id)
                        tao_luong_ngay(nhanvien.id)
            except Exception as e:
                print(e)


@receiver(m2m_changed, sender=GanCongDoan.CongDoan.through)
def gancongdoan_congdoan_changed(sender, instance, action, **kwargs):
    actions = ["post_add", "post_remove", "post_clear", "post_save"]
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


def tao_so_luong_moi_gio(nhanvien_id, cong_doan_id, san_pham_id):
    try:
        SoLuongMoiGio.objects.get(NhanVien_id=nhanvien_id, CongDoan_id=cong_doan_id, SanPham_id=san_pham_id)
    except:
        SoLuongMoiGio.objects.create(NhanVien_id=nhanvien_id, CongDoan_id=cong_doan_id, SanPham_id=san_pham_id)


def tao_luong_ngay(nhanvien_id):
    if LuongNgayNhanVien.objects.filter(NhanVien_id=nhanvien_id, created_at__date=date.today()).exists():
        pass
    else:
        try:
            ngay_hom_qua = date.today() - timedelta(1)
            luong_hom_qua = LuongNgayNhanVien.objects.get(NhanVien_id=nhanvien_id, created_at=ngay_hom_qua)
            LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id,
                                             LuongNgayHomTruoc=luong_hom_qua.LuongNgayHomTruoc)
        except:
            LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id)


def update_so_luong_lam(gan_obj, nhanvien_id, cong_them):
    try:
        so_luong_lam = SoLuongLam.objects.get(NhanVien_id=nhanvien_id, SanPham_id=gan_obj.GanCongDoan.TenSanPham_id)
        if cong_them:
            so_luong_lam.TongThoiGianCuaNhanVien += gan_obj.CongDoan.ThoiGianHoanThanh
            so_luong_lam.GiaCongDoan += gan_obj.CongDoan.DonGia
        else:
            so_luong_lam.TongThoiGianCuaNhanVien -= gan_obj.CongDoan.ThoiGianHoanThanh
            so_luong_lam.GiaCongDoan -= gan_obj.CongDoan.DonGia
        so_luong_lam.LuongNgay = so_luong_lam.GiaCongDoan * gan_obj.GanCongDoan.SoLuong1Ngay
        so_luong_lam.SoLuongToiThieu = round(
            8 * 60 * 60 / so_luong_lam.TongThoiGianCuaNhanVien)
        so_luong_lam.LuongNgayToiThieu = so_luong_lam.SoLuongToiThieu * so_luong_lam.GiaCongDoan
        so_luong_lam.SoLuongDatTiepTheo = so_luong_lam.SoLuongToiThieu * Decimal(
            20 / 100) + so_luong_lam.SoLuongToiThieu
        so_luong_lam.LuongKhiDatSoTiepTheo = so_luong_lam.GiaCongDoan * Decimal(
            so_luong_lam.SoLuongDatTiepTheo)
        so_luong_lam.KichCauDeTangLuong = Decimal(
            so_luong_lam.SoLuongDatTiepTheo) - so_luong_lam.SoLuongToiThieu
        so_luong_lam.save()
        return True
    except:
        return False


@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    if created:
        NhanVien.objects.create(User=instance)


@receiver(post_save, sender=User)
def save_staff(sender, instance, **kwargs):
    if instance.first_name and instance.last_name:
        nhanvien = NhanVien.objects.get(User=instance)
        nhanvien.Ho = instance.first_name
        nhanvien.Ten = instance.last_name
        nhanvien.save()


@receiver(post_save, sender=NhanVien)
def save_staff(sender, instance, created, **kwargs):
    if created:
        try:
            if instance is not None:
                with transaction.atomic():
                    new_user = User.objects.create(username=str(instance.SoDienThoai))
                    new_user.set_password(str(instance.SoDienThoai))
                    new_user.save()
                    instance.user = new_user
        except:
            pass


@receiver(post_delete, sender=NhanVien)
def delete_staff(sender, instance, **kwargs):
    try:
        user = User.objects.get(id=instance.User_id)
        user.delete()
    except:
        pass
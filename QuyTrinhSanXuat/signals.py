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


@receiver(post_save, sender=SoLuongLam)
def tao_so_luong_lam(sender, instance, created, **kwargs):
    if created:
        gans = Gan.objects.filter(NhanVien=instance.NhanVien, GanCongDoan__TenSanPham=instance.SanPham)
        gancongdoan = GanCongDoan.objects.get(TenSanPham=instance.SanPham)
        # Chua co gan truoc do
        if not gans.exists():
            instance.LuongNgay = instance.GiaCongDoan * gancongdoan.SoLuong1Ngay
            instance.SoLuongToiThieu = round(8 * 60 * 60 / instance.TongThoiGianCuaNhanVien)
            instance.LuongNgayToiThieu = instance.SoLuongToiThieu * instance.GiaCongDoan
            instance.SoLuongDatTiepTheo = instance.SoLuongToiThieu * Decimal(20 / 100) + instance.SoLuongToiThieu
            instance.LuongKhiDatSoTiepTheo = instance.GiaCongDoan * Decimal(
                instance.SoLuongDatTiepTheo) * constants.PhanTramThuong
        else:
            GiaCongDoan = 0
            for gan in gans:
                TongThoiGianCuaNhanVien = gan.TongThoiGianCuaNhanVien
                GiaCongDoan += gan.CongDoan.DonGia
            instance.TongThoiGian = TongThoiGianCuaNhanVien
            instance.GiaCongDoan = GiaCongDoan
            instance.LuongNgay = GiaCongDoan * gancongdoan.SoLuong1Ngay
            instance.SoLuongToiThieu = round(8 * 60 * 60 / TongThoiGianCuaNhanVien)
            instance.SoLuongDatTiepTheo = instance.SoLuongToiThieu * Decimal(20 / 100) + instance.SoLuongToiThieu
            instance.LuongNgayToiThieu = instance.SoLuongToiThieu * GiaCongDoan
            instance.LuongKhiDatSoTiepTheo = GiaCongDoan * Decimal(
                instance.SoLuongDatTiepTheo) * constants.PhanTramThuong
        instance.GanCongDoan = gancongdoan
        instance.KichCauDeTangLuong = instance.SoLuongDatTiepTheo - instance.SoLuongToiThieu
        instance.save()

        # create Luong Ngay Nhan Vien


@receiver(pre_save, sender=Gan)
def chiacongdoan_changed(sender, instance, **kwargs):
    gan_truoc_do = Gan.objects.get(id=instance.id)
    nhan_vien_truoc = gan_truoc_do.NhanVien
    gans = Gan.objects.filter(NhanVien=nhan_vien_truoc, GanCongDoan=instance.GanCongDoan)
    # Nếu thêm nhân viên vào chia công đoạn
    if gan_truoc_do.NhanVien is None:
        try:
            so_luong_lam = SoLuongLam.objects.get(NhanVien_id=instance.NhanVien_id,
                                                  SanPham_id=instance.GanCongDoan.TenSanPham_id)
            so_luong_lam.TongThoiGianCuaNhanVien += instance.TongThoiGianCuaNhanVien
            so_luong_lam.GiaCongDoan += instance.CongDoan.DonGia
            so_luong_lam.LuongNgayNhanVien = so_luong_lam.GiaCongDoan * instance.GanCongDoan.SoLuong1Ngay
            so_luong_lam.SoLuongToiThieu = round(8 * 60 * 60 / so_luong_lam.TongThoiGianCuaNhanVien)
            so_luong_lam.LuongNgayToiThieu = so_luong_lam.SoLuongToiThieu * so_luong_lam.GiaCongDoan
            so_luong_lam.SoLuongDatTiepTheo = so_luong_lam.SoLuongToiThieu * Decimal(
                    20 / 100) + so_luong_lam.SoLuongToiThieu
            so_luong_lam.LuongKhiDatSoTiepTheo = so_luong_lam.GiaCongDoan * Decimal(
                so_luong_lam.SoLuongDatTiepTheo) * constants.PhanTramThuong
            so_luong_lam.KichCauDeTangLuong = Decimal(
                so_luong_lam.LuongKhiDatSoTiepTheo) - so_luong_lam.LuongNgayToiThieu
            so_luong_lam.save()
        except:
            SoLuongLam.objects.create(NhanVien_id=instance.NhanVien_id,
                                      GiaCongDoan=instance.CongDoan.DonGia,
                                      TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                                      SanPham_id=instance.GanCongDoan.TenSanPham_id)
    # Trường hợp đổi thành None
    elif instance.NhanVien is None:
        so_luong_lam = SoLuongLam.objects.get(NhanVien=nhan_vien_truoc, SanPham=instance.GanCongDoan.TenSanPham)
        if gans.count() > 1:
            so_luong_lam.TongThoiGianCuaNhanVien -= instance.TongThoiGianCuaNhanVien
            so_luong_lam.GiaCongDoan -= instance.CongDoan.DonGia
            so_luong_lam.LuongNgayNhanVien = so_luong_lam.GiaCongDoan * instance.GanCongDoan.SoLuong1Ngay
            so_luong_lam.SoLuongToiThieu = round(8 * 60 * 60 / so_luong_lam.TongThoiGianCuaNhanVien)
            so_luong_lam.LuongNgayToiThieu = so_luong_lam.SoLuongToiThieu * so_luong_lam.GiaCongDoan
            so_luong_lam.SoLuongDatTiepTheo = so_luong_lam.SoLuongToiThieu * Decimal(20 / 100) + so_luong_lam.SoLuongToiThieu
            so_luong_lam.LuongKhiDatSoTiepTheo = so_luong_lam.GiaCongDoan * Decimal(so_luong_lam.SoLuongDatTiepTheo) * constants.PhanTramThuong
            so_luong_lam.KichCauDeTangLuong = so_luong_lam.SoLuongDatTiepTheo - so_luong_lam.LuongNgayToiThieu
            so_luong_lam.save()
        else:
            so_luong_lam.delete()
    # Đổi nhân viên
    else:
        # Chi co 1 gan thi thay the Nhan vien
        if gans.count() == 1:
            so_luong_lam = SoLuongLam.objects.get(NhanVien_id=nhan_vien_truoc.id,
                                                  SanPham_id=instance.GanCongDoan.TenSanPham_id)
            so_luong_lam.NhanVien = instance.NhanVien
            so_luong_lam.save()
        else:
            # check xem đã có số lượng làm trước đó chưa, chưa thì tạo
            try:
                so_luong_lam = SoLuongLam.objects.get(NhanVien_id=instance.NhanVien_id,
                                                      SanPham_id=instance.GanCongDoan.TenSanPham_id)
                # update
                so_luong_lam.TongThoiGianCuaNhanVien += instance.TongThoiGianCuaNhanVien
                so_luong_lam.GiaCongDoan += instance.CongDoan.DonGia
                so_luong_lam.LuongNgayNhanVien = so_luong_lam.GiaCongDoan * instance.GanCongDoan.SoLuong1Ngay
                so_luong_lam.SoLuongToiThieu = round(8 * 60 * 60 / so_luong_lam.TongThoiGianCuaNhanVien)
                so_luong_lam.LuongNgayToiThieu = so_luong_lam.SoLuongToiThieu * so_luong_lam.GiaCongDoan
                so_luong_lam.SoLuongDatTiepTheo = so_luong_lam.SoLuongToiThieu * Decimal(
                            20 / 100) + so_luong_lam.SoLuongToiThieu
                so_luong_lam.LuongKhiDatSoTiepTheo = so_luong_lam.GiaCongDoan * Decimal(
                    so_luong_lam.SoLuongDatTiepTheo) * constants.PhanTramThuong
                so_luong_lam.KichCauDeTangLuong = Decimal(
                    so_luong_lam.LuongKhiDatSoTiepTheo) - so_luong_lam.LuongNgayToiThieu
                so_luong_lam.save()
            except:
                SoLuongLam.objects.create(NhanVien_id=instance.NhanVien_id,
                                          GiaCongDoan=instance.CongDoan.DonGia,
                                          TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                                          SanPham_id=instance.GanCongDoan.TenSanPham_id)

            # update so luong lam nhan vien truoc
            so_luong_lam_nv_truoc = SoLuongLam.objects.get(NhanVien_id=nhan_vien_truoc.id,
                                                           SanPham_id=instance.GanCongDoan.TenSanPham_id)
            so_luong_lam_nv_truoc.TongThoiGianCuaNhanVien -= instance.TongThoiGianCuaNhanVien
            so_luong_lam_nv_truoc.GiaCongDoan -= instance.CongDoan.DonGia
            so_luong_lam_nv_truoc.LuongNgayNhanVien = so_luong_lam_nv_truoc.GiaCongDoan * instance.GanCongDoan.SoLuong1Ngay
            so_luong_lam_nv_truoc.SoLuongToiThieu = round(8 * 60 * 60 / so_luong_lam_nv_truoc.TongThoiGianCuaNhanVien)
            so_luong_lam_nv_truoc.LuongNgayToiThieu = so_luong_lam_nv_truoc.SoLuongToiThieu * so_luong_lam_nv_truoc.GiaCongDoan
            so_luong_lam_nv_truoc.SoLuongDatTiepTheo = so_luong_lam_nv_truoc.LuongNgayToiThieu * Decimal(
                        20 / 100) + so_luong_lam_nv_truoc.LuongNgayToiThieu
            so_luong_lam_nv_truoc.LuongKhiDatSoTiepTheo = so_luong_lam_nv_truoc.GiaCongDoan * Decimal(
                so_luong_lam_nv_truoc.SoLuongDatTiepTheo) * constants.PhanTramThuong
            so_luong_lam_nv_truoc.KichCauDeTangLuong = Decimal(
                so_luong_lam_nv_truoc.SoLuongDatTiepTheo) - so_luong_lam_nv_truoc.LuongNgayToiThieu
            so_luong_lam_nv_truoc.save()


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
                        LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id,
                                                         LuongNgayHomTruoc=luong_hom_qua.LuongNgayHomTruoc)
                    except:
                        LuongNgayNhanVien.objects.create(NhanVien_id=nhanvien_id)
                if SoLuongLam.objects.filter(NhanVien=nhanvien_id, SanPham=instance.TenSanPham_id).exists():
                    nhanvienlam = SoLuongLam.objects.get(NhanVien=nhanvien_id, SanPham=instance.TenSanPham_id)
                    nhanvienlam.GiaCongDoan += congdoan.DonGia
                    nhanvienlam.LuongNgay = nhanvienlam.GiaCongDoan * instance.SoLuong1Ngay
                    nhanvienlam.LuongNgayToiThieu = nhanvienlam.SoLuongToiThieu * nhanvienlam.GiaCongDoan
                    nhanvienlam.save()
                else:
                    SoLuongToiThieu = round(8 * 60 * 60 / nhanvien.get('TongThoiGianCuaNhanVien'))
                    SoLuongDatTiepTheo = SoLuongToiThieu * Decimal(20 / 100) + SoLuongToiThieu
                    GiaCongDoan = congdoan.DonGia
                    SoLuongLam.objects.create(NhanVien=nhanvien_obj, SanPham=san_pham_obj, GanCongDoan=instance,
                                              TongThoiGianCuaNhanVien=nhanvien.get('TongThoiGianCuaNhanVien'),
                                              GiaCongDoan=GiaCongDoan, LuongNgay=GiaCongDoan * instance.SoLuong1Ngay,
                                              SoLuongToiThieu=SoLuongToiThieu,
                                              LuongNgayToiThieu=SoLuongToiThieu * GiaCongDoan,
                                              SoLuongDatTiepTheo=SoLuongDatTiepTheo,
                                              LuongKhiDatSoTiepTheo=GiaCongDoan * Decimal(
                                                  SoLuongDatTiepTheo) * constants.PhanTramThuong,
                                              KichCauDeTangLuong=SoLuongDatTiepTheo - SoLuongToiThieu)


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
def save_staff(sender, instance, created, **kwargs):
    if created:
        a = 'a'

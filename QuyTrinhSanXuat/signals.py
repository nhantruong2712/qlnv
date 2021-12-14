from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from datetime import date, timedelta
from django.db import transaction

from . import constants
from .models import GanCongDoan, CongDoan, Gan, SoLuongLam, SoLuongMoiGio, LuongNgayNhanVien
from .utils import AssignTask
from sanxuat.models import NhanVien, SanPham
from decimal import Decimal
from django.contrib.auth.models import User

# before_save = []


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
        instance.LuongKhiDatSoTiepTheo = GiaCongDoan * Decimal(instance.SoLuongDatTiepTheo) * constants.PhanTramThuong
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
            # before_save.append(nhanvien.id)

    actions = ["post_remove", "post_clear", "post_save", "post_add"]
    if action in actions:
        # # save
        # try:
        # total_time = 0
        # instance_nhanvien = instance.NhanVien.all()
        #     obj = Gan.objects.values('NhanVien', 'TongThoiGianCuaNhanVien').filter(pk=instance.pk)
        #     # Because admin inline manytomany cannot show TongThoiGian of many NhanVien, so check if then continue
        #     if obj.count() == 1:
        #         for nhanvien in obj:
        #             if nhanvien['NhanVien'] is not None:
        #                 gans = Gan.objects.filter(NhanVien__id=nhanvien['NhanVien'], GanCongDoan__id=instance.GanCongDoan.id)
        #                 if gans.count() == 1:
        #                     total_time = instance.TongThoiGianCuaNhanVien + instance.CongDoan.ThoiGianHoanThanh
        #                 else:
        #                     for gan in gans:
        #                         total_time += gan.CongDoan.ThoiGianHoanThanh
        #                 gans.update(TongThoiGianCuaNhanVien=total_time)
        #             else:
        #                 instance.TongThoiGianCuaNhanVien = None
        #         instance.save()
        # except Exception as e:
        #     print(e)
        with transaction.atomic():
            try:
                # list_nhanvien = list(set(before_save))
                instance_nhanvien = instance.NhanVien.all()
                # Đổi từ None sang nhân viên (thêm nhân viên)
                # if len(list_nhanvien) == 0:
                for nhanvien in instance_nhanvien:
                    update = update_so_luong_lam(gan_obj=instance, nhanvien_id=nhanvien.id, cong_them=True)
                    if not update:
                        SoLuongLam.objects.create(NhanVien_id=nhanvien.id,
                                                  GiaCongDoan=instance.CongDoan.DonGia,
                                                  TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                                                  SanPham_id=instance.GanCongDoan.TenSanPham_id)
                        tao_so_luong_moi_gio(nhanvien.id, instance.CongDoan.id, instance.GanCongDoan.TenSanPham_id)
                # else:
                #     for id_nhan_vien_truoc in list_nhanvien:
                #         try:
                #             gans = Gan.objects.filter(NhanVien=id_nhan_vien_truoc, GanCongDoan=instance.GanCongDoan)
                #         except:
                #             gans = None
                #         # Chưa gán nhân viên
                #         if gans is None:
                #             try:
                #                 update_so_luong_lam(gan_obj=instance, nhanvien_id=id_nhan_vien_truoc, cong_them=True)
                #             except:
                #                 SoLuongLam.objects.create(NhanVien_id=id_nhan_vien_truoc,
                #                                           GiaCongDoan=instance.CongDoan.DonGia,
                #                                           TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                #                                           SanPham_id=instance.GanCongDoan.TenSanPham_id)
                #                 tao_so_luong_moi_gio(id_nhan_vien_truoc, instance.CongDoan.id,
                #                                      instance.GanCongDoan.TenSanPham_id)
                        # # Đổi nhân viên
                        # else:
                        #     # Chi co 1 gan thi thay the Nhan vien
                        #     if gans.count() == 1:
                        #         so_luong_lam = SoLuongLam.objects.get(NhanVien_id=id_nhan_vien_truoc,
                        #                                               SanPham_id=instance.GanCongDoan.TenSanPham_id)
                        #         so_luong_lam.NhanVien = instance.NhanVien
                        #         so_luong_lam.save()
                        #     else:
                        #         # check xem đã có số lượng làm trước đó chưa, chưa thì tạo
                        #         try:
                        #             SoLuongLam.objects.get(NhanVien_id=id_nhan_vien_truoc,
                        #                                    SanPham_id=instance.GanCongDoan.TenSanPham_id)
                        #         except:
                        #             SoLuongLam.objects.create(NhanVien_id=instance.NhanVien_id,
                        #                                       GiaCongDoan=instance.CongDoan.DonGia,
                        #                                       TongThoiGianCuaNhanVien=instance.CongDoan.ThoiGianHoanThanh,
                        #                                       SanPham_id=instance.GanCongDoan.TenSanPham_id)
                        #             # Tạo số lượng mỗi giờ
                        #             tao_so_luong_moi_gio(instance.NhanVien_id, instance.CongDoan.id,
                        #                                  instance.GanCongDoan.TenSanPham.id)
                        #         # update so luong lam nhan vien truoc
                        #         update_so_luong_lam(gan_obj=instance, nhanvien_id=id_nhan_vien_truoc, cong_them=False)
            except Exception as e:
                print(e)
        # before_save.clear()


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
                san_pham_obj = SanPham.objects.get(id=instance.TenSanPham_id)
                # Tạo số lượng mỗi giờ
                tao_so_luong_moi_gio(nhanvien_id, congdoan.id, san_pham_obj.id)
                # Tạo Lương Ngày Nhân Viên
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

                # Tạo Số Lượng Làm
                try:
                    nhanvienlam = SoLuongLam.objects.get(NhanVien=nhanvien_id, SanPham=instance.TenSanPham_id)
                    nhanvienlam.GiaCongDoan += congdoan.DonGia
                    nhanvienlam.LuongNgay = nhanvienlam.GiaCongDoan * instance.SoLuong1Ngay
                    nhanvienlam.LuongNgayToiThieu = nhanvienlam.SoLuongToiThieu * nhanvienlam.GiaCongDoan
                    nhanvienlam.save()
                except:
                    SoLuongLam.objects.create(NhanVien_id=nhanvien_id, SanPham=san_pham_obj,
                                              TongThoiGianCuaNhanVien=nhanvien.get('TongThoiGianCuaNhanVien'),
                                              GiaCongDoan=congdoan.DonGia)


def tao_so_luong_moi_gio(nhanvien_id, cong_doan_id, san_pham_id):
    try:
        SoLuongMoiGio.objects.get(NhanVien_id=nhanvien_id, CongDoan_id=cong_doan_id, SanPham_id=san_pham_id)
    except:
        SoLuongMoiGio.objects.create(NhanVien_id=nhanvien_id, CongDoan_id=cong_doan_id, SanPham_id=san_pham_id)


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
            so_luong_lam.SoLuongDatTiepTheo) * constants.PhanTramThuong
        so_luong_lam.KichCauDeTangLuong = Decimal(
            so_luong_lam.SoLuongDatTiepTheo) - so_luong_lam.LuongNgayToiThieu
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
        nhanvien.TenNhanVien = instance.first_name + ' ' + instance.last_name
        nhanvien.save()


@receiver(post_save, sender=NhanVien)
def save_staff(sender, instance, created, **kwargs):
    if created:
        a = 'a'

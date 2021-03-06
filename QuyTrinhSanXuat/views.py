from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from itertools import chain

from QuyTrinhSanXuat.func import thousand_format
from QuyTrinhSanXuat.models import LuongNgayNhanVien, SoLuongLam
from sanxuat.models import SanPham, NhanVien


@login_required(login_url='/login')
def xem_luong(request):
    current_month = datetime.now().month
    try:
        nhan_vien = NhanVien.objects.get(User=request.user)
        ho_ten = nhan_vien.Ho + ' ' + nhan_vien.Ten
    except:
        nhan_vien = request.user
        ho_ten = nhan_vien
    if nhan_vien != request.user:
        luong_thang = LuongNgayNhanVien.objects.filter(NhanVien=nhan_vien,
                                                       created_at__month=current_month).last().LuongThang
        so_luong_lam = SoLuongLam.objects.filter(NhanVien=nhan_vien).order_by('-id')
        # luong_ngay = LuongNgayNhanVien.objects.filter(NhanVien=nhan_vien).order_by('-id')
        # result_list = list(chain(luong_ngay, so_luong_lam))
    else:
        luong_thang = 0
        so_luong_lam = None
        # luong_ngay = None
        # result_list = []
    context = {'ho_ten': ho_ten, 'nhan_vien': nhan_vien, 'luong_thang': luong_thang,
               'so_luong_lam': so_luong_lam}
    return render(request, 'QuyTrinhSanXuat/dt-basic.html', context)


@login_required(login_url='/login')
@staff_member_required
def index(request):
    # admin
    admin = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    so_luong_admin = admin.count()
    admin_moi_nhat = admin.order_by('-id')[:5]
    # san pham
    san_pham = SanPham.objects.filter(hoan_tat=False)
    so_san_pham = san_pham.count()
    san_pham_moi_nhat = san_pham.order_by('-id')[:5]
    context = {"so_luong_admin": so_luong_admin, "so_luong_san_pham": so_san_pham, 'admin_moi_nhat': admin_moi_nhat,
               "san_pham_moi_nhat": san_pham_moi_nhat}
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat.html', context)


@staff_member_required
def admin_list(request):
    all_admin = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    return render(request, 'QuyTrinhSanXuat/admin_list.html', context={'admin_list': all_admin})


@staff_member_required
def doitacsanxuat_list(request):
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat_list.html')


@staff_member_required
def khachhang(request):
    return render(request, 'QuyTrinhSanXuat/khachhang.html')


@staff_member_required
def nhanvien_list(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_list.html')


@staff_member_required
def nhanvien_cong(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_cong.html')


@staff_member_required
def duan_list(request):
    return render(request, 'QuyTrinhSanXuat/duan.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to previous page after login
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    if not request.user.is_staff:
                        return redirect('/luong')
                    return redirect('/')
            else:
                messages.error(request, "Sai t??n ????ng nh????p ho????c m????t kh????u")
    context = {}
    return render(request, 'QuyTrinhSanXuat/login.html', context)


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect('/login')

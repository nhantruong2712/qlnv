from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import CreateView
from QuyTrinhSanXuat.models import GanCongDoan
# Create your views here.from django import forms
from sanxuat.models import SanPham


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


def admin_list(request):
    all_admin = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    return render(request, 'QuyTrinhSanXuat/admin_list.html', context={'admin_list': all_admin})


def doitacsanxuat_list(request):
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat_list.html')


def khachhang(request):
    return render(request, 'QuyTrinhSanXuat/khachhang.html')


def nhanvien_list(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_list.html')


def nhanvien_cong(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_cong.html')


def duan_list(request):
    return render(request, 'QuyTrinhSanXuat/duan.html')
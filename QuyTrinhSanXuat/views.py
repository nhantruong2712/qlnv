from django.shortcuts import render
from django.views.generic import CreateView
from QuyTrinhSanXuat.models import GanCongDoan
# Create your views here.from django import forms


def index(request):
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat.html')


def admin_list(request):
    return render(request, 'QuyTrinhSanXuat/admin_list.html')


def doitacsanxuat_list(request):
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat_list.html')


def khachhang(request):
    return render(request, 'QuyTrinhSanXuat/khachhang.html')


def nhanvien_list(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_list.html')


def nhanvien_cong(request):
    return render(request, 'QuyTrinhSanXuat/nhanvien_cong.html')
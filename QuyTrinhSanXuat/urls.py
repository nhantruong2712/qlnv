from django.urls import path
from . import views

app_name = 'QuyTrinhSanXuat'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-list/', views.admin_list, name='admin_list'),
    path('doitacsanxuat/lists/', views.doitacsanxuat_list, name='doitacsanxuat_list'),
    path('khachhang/', views.khachhang, name='khachhang'),
    path('nhanvien/lists/', views.nhanvien_list, name='nhanvien_list'),
    path('nhanvien/cong/', views.nhanvien_cong, name='nhanvien_cong'),
    path('duan-list/', views.duan_list, name='duan_list'),
]
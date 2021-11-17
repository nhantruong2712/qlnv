from django.shortcuts import render
from django.views.generic import CreateView
from QuyTrinhSanXuat.models import GanCongDoan
# Create your views here.from django import forms


def index(request):
    return render(request, 'QuyTrinhSanXuat/doitacsanxuat.html')
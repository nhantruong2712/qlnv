from django.urls import path
from . import views

app_name = 'QuyTrinhSanXuat'

urlpatterns = [
    path('', views.index, name='index')
]
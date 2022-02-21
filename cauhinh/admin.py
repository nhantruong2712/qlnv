from typing import Text
from django.contrib import admin
from .models import *


class CauHinhChungAdmin(admin.ModelAdmin):
    list_display = ('phantramthuong',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(bactho)
admin.site.register(phongban)
admin.site.register(chucvu)
admin.site.register(thietbi)
admin.site.register(CauHinhChung, CauHinhChungAdmin)


# Register your models here.

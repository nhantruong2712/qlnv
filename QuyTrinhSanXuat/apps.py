from django.apps import AppConfig


class QuytrinhsanxuatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QuyTrinhSanXuat'

    def ready(self):
        import QuyTrinhSanXuat.signals

# import os
# import pathlib
# from datetime import datetime, timedelta
#
# from django.core.files import File
# from django.utils import timezone
# from extra_settings.models import Setting
#
# from rosenbridge import settings
# from rosenbridge.mta.models import PatientFile, Patient
# from rosenbridge.utils.share_point import SharePointHelper
# from rosenbridge.patient.models import TransferRequest
# from rosenbridge.app_celery import app
# from rosenbridge.utils.shortcuts import get_or_none
# 
#
# @app.task(name='MedScan.Share_Patient_Items')
# def share_patient_item():
#     transfer_items = TransferRequest.objects.filter(
#         status=TransferRequest.TransferRequestStatus.SCHEDULED,
#         file_status=TransferRequest.DownloadFileStatus.DOWNLOADED,
#     )
#     for item in transfer_items:
#         try:
#             TransferRequest.objects.share(item.id)
#         except Exception as e:
#             item.error_log = '%s (%s)' % (e.message, type(e))
#             item.save()
#
#
# @app.task(name='MedScan.Download_Patient_Folder')
# def download_patient_folder(unique_id: str, relative_url: str):
#     transfer_request = get_or_none(TransferRequest, unique_id=unique_id)
#     if not transfer_request:
#         raise Exception("unique_id not found: %s" % unique_id)
#     try:
#         transfer_request.file_status = TransferRequest.DownloadFileStatus.DOWNLOADING
#         transfer_request.save()
#         #
#         download_folder_path = os.path.join(settings.MEDIA_ROOT, settings.SHAREPOINT_DOWNLOADED_PATIENT_FOLDER)
#         pathlib.Path(download_folder_path).mkdir(parents=True, exist_ok=True)
#         download_file = "%s/%s.zip" % (settings.SHAREPOINT_DOWNLOADED_PATIENT_FOLDER, unique_id)
#         file_path = "%s/%s" % (settings.MEDIA_ROOT, download_file)
#         #
#         share_point = SharePointHelper()
#         share_point.zip_entire_folder(relative_url, file_path)
#         #
#         transfer_request.file_status = TransferRequest.DownloadFileStatus.DOWNLOADED
#         transfer_request.downloaded_file = download_file
#         transfer_request.save()
#         return file_path
#     except Exception as e:
#         transfer_request.file_status = TransferRequest.DownloadFileStatus.ERROR
#         transfer_request.error_log = '%s (%s)' % (e.message, type(e))
#         transfer_request.save()
#         pass
#
#
# @app.task(name='MedScan.Sync_Transfer_Item')
# def sync_patient_transfer_item(relative_url: str):
#     try:
#         share_point = SharePointHelper()
#         transfer_item = share_point.get_folder_by_relative_url(relative_url)
#         if not transfer_item:
#             raise Exception("Folder not found: %s" % relative_url)
#
#         transfer_request = TransferRequest.objects.create_or_update(transfer_item)
#         # Download folder/files from SharePoint
#         download_patient_folder.delay(transfer_request.unique_id, transfer_request.relative_url)
#
#         return relative_url
#     except Exception as e:
#         print("Error: sync_patient_transfer_item")
#         raise e
#
#
# @app.task(name='MedScan.Resend_Transfer_Items')
# def resend_patient_transfer_items():
#     try:
#         resend_items = TransferRequest.objects.filter(is_resend=True, file_status=TransferRequest.DownloadFileStatus.DOWNLOADED)
#         for item in resend_items:
#             patient = Patient.objects.get(
#                 transfer=item.transfer
#             )
#             patient_name = "%s %s" % (item.patient_first_name, item.patient_last_name)
#             download_folder_path = os.path.join(settings.MEDIA_ROOT, item.downloaded_file)
#             file_name = "%s.zip" % patient_name.replace(" ", "_")
#             try:
#                 with open(download_folder_path, 'rb') as patient_file:
#                     patient_file = PatientFile.objects.create(
#                         patient=patient,
#                         encrypted_file=File(patient_file, file_name)
#                     )
#             except Exception as e:
#                 raise e
#             item.transfer.send_email(transfer_request=item)
#             item.is_resend = False
#             item.save()
#             os.remove(download_folder_path)
#     except Exception as e:
#         print("Error: resend_patient_transfer_item")
#         raise e
#
#
# @app.task(name='MedScan.Sync_Transfer_Requests')
# def sync_patient_transfer_requests():
#     try:
#         filter_date = datetime.now(tz=timezone.utc) - timedelta(1)
#         last_sync = Setting.get(settings.SHAREPOINT_LAST_SYNC_KEY, default=filter_date)
#
#         share_point = SharePointHelper()
#         modified_folders = share_point.get_modified_folders(last_sync)
#         for folder in modified_folders:
#             transfer_request = TransferRequest.objects.create_or_update(folder)
#             # Download folder/files from SharePoint
#             download_patient_folder.delay(transfer_request.unique_id, transfer_request.relative_url)
#
#         # Update last synced time
#         stored_setting = get_or_none(Setting, name=settings.SHAREPOINT_LAST_SYNC_KEY, value_type=Setting.TYPE_DATETIME)
#         if stored_setting:
#             stored_setting.value_datetime = datetime.now(tz=timezone.utc)
#         else:
#             stored_setting = Setting(
#                 name=settings.SHAREPOINT_LAST_SYNC_KEY,
#                 value_type=Setting.TYPE_DATETIME,
#                 value_datetime=datetime.now(tz=timezone.utc)
#             )
#         stored_setting.save()
#
#     except Exception as e:
#         print("Error: sync_patient_transfer_requests")
#         raise e
#
#
# import os
# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
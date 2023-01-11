# Librerías de Terceros
from django.urls import path
from .payments_batch_views import FilePaymentsUploadView, file_progress_updates


upload_file = {"post": "upload_file"}
get_uploaded_files={'get':'get_uploaded_files'}
get_file_details={'get':'get_file_details'}
apply_file_payments={'patch':'apply_file_recipients'}

urlpatterns = [
    path('batch-payments/upload-file/', FilePaymentsUploadView.as_view(
        {
            **upload_file,
            **get_uploaded_files
        }
    ), name='payment-upload-file'),
    path('batch-payments', FilePaymentsUploadView.as_view(
            {
                **get_file_details,
                **apply_file_payments,
            }
        ), name='batch-recipients'),
    path('batch-payments/progress/<str:task_id>/', file_progress_updates, name='file-progress'),

]

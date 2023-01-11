# Librerías de Terceros
from django.urls import path
from .recipients_batch_views import FileUploadView, file_progress_updates


upload_file = {"post": "upload_file"}
get_uploaded_files={'get':'get_uploaded_files'}
get_file_details={'get':'get_file_details'}
apply_file_recipients={'patch':'apply_file_recipients'}
delete_file_uploaded={'delete':'delete_file_uploaded'}

urlpatterns = [
    path('batch-recipients/upload-file/', FileUploadView.as_view(
        {
            **upload_file,
            **get_uploaded_files
        }
    ), name='recipient-upload-file'),
    path('batch-recipients', FileUploadView.as_view(
            {
                **get_file_details,
                **apply_file_recipients,
                **delete_file_uploaded
            }
        ), name='batch-recipients'),
    path('batch-recipients/progress/<str:task_id>/', file_progress_updates, name='file-progress'),

]

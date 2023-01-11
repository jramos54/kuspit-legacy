# Librerías de Terceros
from django.urls import path

# Proyecto
from .mockapi_openfin_documents_views import OpenFinDocumentsViewSet
from .documentos_views import FileUploadViewSet

# documents
upload_documents = {"post": "upload_documents"}

# openfin
cat_documents = {"get": "openfin_list_cat_documents"}
upload_document = {"post": "openfin_upload_document"}

urlpatterns = [
    path(
        "documents/<int:doc_type>",
        FileUploadViewSet.as_view(
            {
                **upload_documents,
            }
        ),
        name="documents",
    ),
    path(
        "openfin/documents",
        OpenFinDocumentsViewSet.as_view(
            {
                **cat_documents,
            }
        ),
        name="openfin_list_cat_documents",
    ),
    path(
        "openfin/rpc/documents",
        OpenFinDocumentsViewSet.as_view(
            {
                **upload_document,
            }
        ),
        name="openfin_upload_document",
    ),
]

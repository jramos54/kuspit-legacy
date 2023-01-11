"""url's for frequent questions service"""
# Librerias de Terceros
# Librerías de Terceros
from django.urls import path

# Proyecto
from .frequent_questions_views import (
    FrequentQuestionsAuthViewSet,
    FrequentQuestionsViewSet,
)

# Frequent question without auth
list_frequent_questions = {"get": "list_frequent_questions"}
# Frequent question with auth
create_frequent_questions = {"post": "create_frequent_questions"}
update_frequent_questions = {"put": "update_frequent_questions"}

urlpatterns = [
    path(
        "frequent_questions",
        FrequentQuestionsViewSet.as_view(
            {
                **list_frequent_questions,
            }
        ),
        name="list-frequent-questions",
    ),
    path(
        "frequent_questions_auth",
        FrequentQuestionsAuthViewSet.as_view(
            {
                **create_frequent_questions,
                **update_frequent_questions,
            }
        ),
        name="crud-frequent-questions",
    ),
]

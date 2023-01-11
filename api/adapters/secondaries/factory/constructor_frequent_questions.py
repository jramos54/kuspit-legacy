"""constructor for frequent questions"""
from api.adapters.secondaries.db_orm.repository_implementation_frequen_questions import (
    FrequentQuestions as FrequentQuestionsORM,
)
from api.engine.use_cases.ports.secondaries import (
    repository_frequent_questions as repository,
)

# orm
from apps.webApp.models import frequent_questions as models_frequent_questions


def constructor_frequent_questions(
    frequent_questions_orm_model: models_frequent_questions.FrequentQuestions,
) -> repository.FrequentQuestionsRepository:
    """fuction to retunr the orm of frequent questions"""
    return FrequentQuestionsORM(
        frequent_questions_orm_model=frequent_questions_orm_model
    )

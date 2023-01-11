"""constructor manager for frequent questions engine"""
from api.engine.use_cases.ports.secondaries import (
    repository_frequent_questions as repository,
)
from api.engine.use_cases.ports.primaries import manager_frequent_questions as manager
from api.engine.use_cases.services import service_frequent_questions as service


def constructor_manager_frequent_questions(
    frequent_questions_repository: repository.FrequentQuestionsRepository,
) -> manager.FrequentQuestionsManager:
    """fuction to return the service of frequent question"""
    return service.FrequentQuestionsService(
        frequent_questions_repository=frequent_questions_repository
    )

"""service for frequent question engine"""
# Librerias Estandar
import typing
from dataclasses import dataclass

# Librerias Proyecto
from api.engine.use_cases.ports.secondaries import (
    repository_frequent_questions as repository,
)
from api.engine.use_cases.ports.primaries import manager_frequent_questions as manager
from api.engine.domain.entities import entities_frequent_questions as entity


@dataclass
class FrequentQuestionsService(manager.FrequentQuestionsManager):
    """class to define the service for frequent question engine"""

    def __init__(
        self, frequent_questions_repository: repository.FrequentQuestionsRepository
    ):
        self.frequent_questions_repository = frequent_questions_repository

    def list_frequent_questions(self) -> typing.List[entity.FrequentQuestions]:
        return self.frequent_questions_repository.list_frequent_questions()

    def get_frequent_questions(self, id: int) -> entity.FrequentQuestions:
        frequent_question = self.frequent_questions_repository.get_frequent_questions(
            id=id
        )
        return frequent_question

    def create_frequent_questions(
        self, answer: str, question: str, is_active: bool
    ) -> entity.FrequentQuestions:
        frequent_questions = (
            self.frequent_questions_repository.create_frequent_questions(
                answer=answer, question=question, is_active=is_active
            )
        )
        return frequent_questions

    def update_frequent_questions(
        self,
        id: int,
        answer: typing.Optional[str],
        question: typing.Optional[str],
        is_active: bool,
    ) -> entity.FrequentQuestions:
        frequent_questions = (
            self.frequent_questions_repository.update_frequent_questions(
                id=id,
                question=question,
                answer=answer,
                is_active=is_active,
            )
        )
        return frequent_questions

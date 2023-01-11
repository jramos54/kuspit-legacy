"""Repository implementation for frequent questions engine"""
# Librerias Estandar
# Librerias Estandar
import typing

# engine
from api.engine.use_cases.ports.secondaries import (
    repository_frequent_questions as repository,
)
from api.engine.use_cases.factory import orm_mapper
from api.engine.domain.entities import entities_frequent_questions as entity

# orm
from apps.webApp.models import frequent_questions as models_frequent_questions


class FrequentQuestions(repository.FrequentQuestionsRepository):
    """class for frequent questions entities crud"""

    def __init__(
        self, frequent_questions_orm_model: models_frequent_questions.FrequentQuestions
    ):
        self._frequent_questions_orm_model = frequent_questions_orm_model

    def list_frequent_questions(self) -> typing.List[entity.FrequentQuestions]:
        """fuction for list the entity of frequent questions"""
        return [
            orm_mapper.constructor_frequent_questions_entities(frequent_question)
            for frequent_question in self._frequent_questions_orm_model.objects.all()
        ]

    def get_frequent_questions(self, id: int) -> entity.FrequentQuestions:
        """fuction to get the entity of 1 frequent question"""
        frequent_question = self._frequent_questions_orm_model.objects.get(id=id)
        return orm_mapper.constructor_frequent_questions_entities(frequent_question)

    def create_frequent_questions(
        self, answer: str, question: str, is_active: bool
    ) -> entity.FrequentQuestions:
        """fuction to create the entity of 1 frequent questions"""
        frequent_question = self._frequent_questions_orm_model.objects.create(
            question=question,
            answer=answer,
            is_active=is_active,
        )
        return orm_mapper.constructor_frequent_questions_entities(frequent_question)

    def update_frequent_questions(
        self,
        id: int,
        answer: typing.Optional[str],
        question: typing.Optional[str],
        is_active: bool,
    ) -> entity.FrequentQuestions:
        """fuction to update the entity of 1 frequent questions"""
        frequent_question = self._frequent_questions_orm_model.objects.get(id=id)
        frequent_question.answer = answer if answer else frequent_question.answer
        frequent_question.question = (
            question if question else frequent_question.question
        )
        frequent_question.is_active = is_active

        frequent_question.save(
            update_fields=[
                "answer",
                "question",
                "is_active",
            ]
        )

        return orm_mapper.constructor_frequent_questions_entities(frequent_question)

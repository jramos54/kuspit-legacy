"""Secondaries ports for frequent questios engine"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_frequent_questions as entity


class FrequentQuestionsRepository(abc.ABC):
    """clas to define the repository of frequent question engine"""

    @abc.abstractmethod
    def list_frequent_questions(self) -> typing.List[entity.FrequentQuestions]:
        ...

    @abc.abstractmethod
    def get_frequent_questions(self, id: int) -> entity.FrequentQuestions:
        ...

    @abc.abstractmethod
    def create_frequent_questions(
        self,
        question: str,
        answer: str,
        is_active: bool,
    ) -> entity.FrequentQuestions:
        ...

    @abc.abstractmethod
    def update_frequent_questions(
        self,
        id: int,
        answer: typing.Optional[str],
        question: typing.Optional[str],
        is_active: bool,
    ) -> entity.FrequentQuestions:
        ...

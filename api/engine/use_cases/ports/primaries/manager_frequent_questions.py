"""Primarie ports for frequent questions engine"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_frequent_questions as entity


class FrequentQuestionsManager(abc.ABC):
    """class to define the manager for frequent questions engine"""

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
        id: typing.Optional[int],
        question: typing.Optional[str],
        answer: typing.Optional[str],
        is_active: typing.Optional[bool],
    ) -> entity.FrequentQuestions:
        ...

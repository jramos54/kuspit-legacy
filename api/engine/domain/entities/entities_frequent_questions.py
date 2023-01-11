"""Entities for frequent questions"""
# Librerias Estandar
import typing
from dataclasses import dataclass


@dataclass
class FrequentQuestions:
    """class to define the entities of frequent questions"""

    id: int
    answer: typing.Optional[str]
    question: typing.Optional[str]
    is_active: bool

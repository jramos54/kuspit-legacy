"""Exceptions for frequent questions service"""
from compartidos.exceptions import ExceptionBase


class QuestionAlreadyExist(ExceptionBase):
    """Question already exist"""

    def __init__(self, frequent_questions_question: str):
        self.frequent_questions_question = frequent_questions_question
        self.message = {
            "detail": f"La siguiente pregunta: {self.frequent_questions_question}, ya existe."
        }


class QuestionNoExist(ExceptionBase):
    """Question not exist"""

    def __init__(self, frequent_questions_id: int):
        self.frequent_questions_id = frequent_questions_id
        self.message = {
            "detail": f"La pregunta con el id: {self.frequent_questions_id}, no existe."
        }

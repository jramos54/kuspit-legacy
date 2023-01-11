"""frequen question models"""
# Librerías de Terceros
from django.db import models


class FrequentQuestions(models.Model):
    """model for frequent question"""

    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Frequent Questions"

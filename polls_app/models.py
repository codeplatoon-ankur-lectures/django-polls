from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=128)
    # choices

    def __str__(self):
        return f"QUESTION: {self.question_text}"

class Choice(models.Model):
    choice_text = models.CharField(max_length=64)
    votes = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return f"CHOICE: {self.choice_text}"

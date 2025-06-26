from django.db import models
from django.contrib.auth.models import User

class CyberVigilanceTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    responses = models.JSONField()
    score = models.IntegerField()
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test de vigilance - Score: {self.score}"

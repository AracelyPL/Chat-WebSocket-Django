from django.db import models
from django.utils.timezone import now

class Message(models.Model):
    user = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"
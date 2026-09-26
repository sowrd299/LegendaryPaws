from django.db import models
from django.contrib.auth.models import User

class SaveState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='save_state')
    state = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SaveState for {self.user.username}"

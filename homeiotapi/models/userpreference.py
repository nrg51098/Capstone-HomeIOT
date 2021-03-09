from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class UserPreference(models.Model):
    
    UNIT_SYSTEM_CHOICES = [
        ('SI', 'Imperial'),
        ('IN', 'Metric'),
    ]
    unit = models.CharField(
        max_length=2,
        choices=UNIT_SYSTEM_CHOICES,
        default = 'IN',
    )

    appuser = models.ForeignKey(
        "AppUser",
        on_delete=CASCADE,
        related_name="userpreferences",
        related_query_name="userpreference"
    )
    fail_notification = models.BooleanField(default=False)
    threshold_notification = models.BooleanField(default=False)
  
    def __str__(self):
        return self.appuser.user.username + " - preferences"
    
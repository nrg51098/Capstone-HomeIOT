from django.db import models
from django.db.models.deletion import CASCADE


class ButtonThreshold(models.Model):
    
    subscription = models.ForeignKey(
        "Subscription",
        on_delete=CASCADE,
        related_name="buttonthresholds",
        related_query_name="buttonthreshold"
    )
    notify_if = models.BooleanField(default = False)

      
    def __str__(self):
      return self.subscription.appuser.user.username + " - Button threshold"
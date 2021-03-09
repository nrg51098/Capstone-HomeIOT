from django.db import models
from django.db.models.deletion import CASCADE


class TempThreshold(models.Model):
    
    subscription = models.ForeignKey(
        "Subscription",
        on_delete=CASCADE,
        related_name="tempthresholds",
        related_query_name="tempthreshold"
    )
    min_temp = models.DecimalField(max_digits = 7, decimal_places = 3)
    max_temp = models.DecimalField(max_digits = 7, decimal_places = 3)

      
    def __str__(self):
      return self.subscription.appuser.user.username + " - Temp threshold"
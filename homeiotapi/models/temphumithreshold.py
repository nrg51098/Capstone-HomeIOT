from django.db import models
from django.db.models.deletion import CASCADE


class TempHumiThreshold(models.Model):
    
    subscription = models.ForeignKey(
        "Subscription",
        on_delete=CASCADE,
        related_name="tempHumithresholds",
        related_query_name="tempHumithreshold"
    )
    min_temp = models.DecimalField(max_digits = 7, decimal_places = 3)
    max_temp = models.DecimalField(max_digits = 7, decimal_places = 3)
    min_humi = models.DecimalField(max_digits = 7, decimal_places = 3)
    max_humi = models.DecimalField(max_digits = 7, decimal_places = 3)

      
    def __str__(self):
      return self.subscription.appuser.user.username + " - Humi threshold"
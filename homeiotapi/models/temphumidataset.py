from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class TempHumiDataset(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    device = models.ForeignKey(
        "Device",
        on_delete=CASCADE,
        related_name="temphumidatasets",
        related_query_name="temphumidataset"
    )
    temp = models.DecimalField(max_digits = 7, decimal_places = 3)
    humi = models.DecimalField(max_digits = 7, decimal_places = 3)

      
    def __str__(self):
      return self.device.name + " - dataset " + str(self.id)
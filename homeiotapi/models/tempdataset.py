from django.db import models
from django.db.models.deletion import CASCADE


class TempDataset(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(
        "Device",
        on_delete=CASCADE,
        related_name="tempdatasets",
        related_query_name="tempdataset"
    )
    temp = models.DecimalField(max_digits = 7, decimal_places = 3)
      
    def __str__(self):
      return self.device.name + " - dataset " + str(self.id)
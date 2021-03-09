from django.db import models
from django.db.models.deletion import CASCADE


class ButtonDataset(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(
        "Device",
        on_delete=CASCADE,
        related_name="buttondatasets",
        related_query_name="buttondataset"
    )
    is_on = models.BooleanField(default = False)

      
    def __str__(self):
      return self.device.name + " - dataset " + str(self.id)
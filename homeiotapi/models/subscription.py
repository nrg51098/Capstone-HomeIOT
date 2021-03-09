from django.db import models
from django.db.models.deletion import CASCADE


class Subscription(models.Model):
    
    sub_unsub_date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(
        "Device",
        on_delete=CASCADE,
        related_name="subscriptions",
        related_query_name="subscription"
    )
    appuser = models.ForeignKey(
        "AppUser",
        on_delete=CASCADE,
        related_name="subscriptions",
        related_query_name="subscription"
    )
    
  
    def __str__(self):
      return self.appuser.user.username + " : " + self.device.name + " - subscription"
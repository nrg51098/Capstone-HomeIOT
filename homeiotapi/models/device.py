from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class Device(models.Model):
    name = models.CharField(max_length=75)
    created_datetime = models.DateTimeField(auto_now_add=True)
    device_img_url = models.CharField(max_length=255)
    hardware_number = models.CharField(max_length=255)
    appuser = models.ForeignKey(
        "AppUser",
        on_delete=CASCADE,
        related_name="devices",
        related_query_name="device"
    )
    location = models.ForeignKey(
        "Location",
        on_delete=SET_NULL,
        # did not add CASCADE here, so device stays even after category is deleted
        related_name="devices",
        related_query_name="device",
        null=True,  # added here if the category was deleted
        blank=True
    )    
    sensor_type = models.ForeignKey(
        "SensorType",
        on_delete=SET_NULL,
        # did not add CASCADE here, so device stays even after category is deleted
        related_name="devices",
        related_query_name="device",
        null=True,  # added here if the category was deleted
        blank=True
    )
    tag = models.ManyToManyField(
        "Tag",
        related_name="tag_devices",
        related_query_name="tag_device"
    )
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
  
    def __str__(self):
      return self.name
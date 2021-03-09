from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class AppUser(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
  address = models.CharField(max_length=255)
  profile_img_url = models.CharField(max_length=255)
  created_on = models.DateField(auto_now_add=True)

  def __str__(self):
      return self.user.username
  
  
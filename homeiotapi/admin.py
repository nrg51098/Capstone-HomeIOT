from django.contrib import admin
from homeiotapi.models import Device,Tag,Location,AppUser,SensorType
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Tag)
admin.site.register(Device)
admin.site.register(Location)
admin.site.register(SensorType)
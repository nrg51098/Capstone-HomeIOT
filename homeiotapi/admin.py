from django.contrib import admin
from homeiotapi.models import Device,Tag,Location,AppUser,SensorType,Subscription, UserPreference, TempDataset, TempHumiDataset, ButtonDataset, TempThreshold, TempHumiThreshold, ButtonThreshold
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Tag)
admin.site.register(Device)
admin.site.register(Location)
admin.site.register(SensorType)
admin.site.register(Subscription)
admin.site.register(UserPreference)
admin.site.register(TempDataset)
admin.site.register(TempHumiDataset)
admin.site.register(ButtonDataset)
admin.site.register(TempThreshold)
admin.site.register(TempHumiThreshold)
admin.site.register(ButtonThreshold)


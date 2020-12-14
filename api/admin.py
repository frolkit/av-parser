from django.contrib import admin

from .models import Item, ItemHistory, Location, Ad


admin.site.register(Item)
admin.site.register(ItemHistory)
admin.site.register(Location)
admin.site.register(Ad)

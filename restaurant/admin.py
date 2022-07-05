from django.contrib import admin
from .models import Table, WaiterOrderPad, Category, MenuItem, OrderedItem

# Register your models here.
admin.site.register(Table)
admin.site.register(WaiterOrderPad)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(OrderedItem)

from django.contrib import admin
from . import models

class ItemOrderInline(admin.TabularInline):
    model = models.ItemOrder
    extra = 1
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemOrderInline
    ]

# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.ItemOrder)
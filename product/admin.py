from django.contrib import admin
from . import models
# Register your models here.

class OptionInLine(admin.TabularInline):
    model = models.Option
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description', 'get_price_formatted', 'get_price_promotional_formatted']
    inlines = [
        OptionInLine
    ]

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Option)
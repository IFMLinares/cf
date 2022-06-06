from django.contrib import admin
from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'sale_price',
        'stock',
        'sku_code',
    )
    # list_filter = ('ocultar', 'departamento', 'tallas', 'categoria')
    search_fields = ['description','sale_price', 'stock','sku_code',]
    list_editable = ['stock']

    list_per_page = 10
    


admin.site.register(Item, ItemAdmin)

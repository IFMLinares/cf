from django.contrib import admin
from .models import Item, OrderItem, Order 

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

class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'totalOrden',
    )
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'totalItem',
    )



admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

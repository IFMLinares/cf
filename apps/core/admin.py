from django.contrib import admin
from .models import Item, OrderItem, Order, Address, User

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

class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone',
    )
    list_per_page = 10

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)


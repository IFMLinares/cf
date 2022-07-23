from django.contrib import admin
from django.utils.html import format_html
from django.forms import SelectMultiple
from django.db import models
from .models import Item, OrderItem, Order, Address, User, BillingAddress, ColorItem, CantItem

# Register your models here.
# class ColorItemAdmin(admin.ModelAdmin):
#     list_display = (
#         'color_name',
#     )
# class CantItemAdmin(admin.ModelAdmin):
#     list_display = (
#         'piezas',
#     )

class ItemAdmin(admin.ModelAdmin):
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'style': 'height: 180%; width: 50%;'})}, }
    list_display = (
        'sku_code',
        'description',
        'sale_price',
        'category',
        'stock',
        'outstanding',
        'imageProduct'
    )
    # list_filter = ('ocultar', 'departamento', 'tallas', 'categoria')
    # search_fields = ['description', 'sale_price',
    #                  'stock', 'sku_code', 'category', 'outstanding']
    list_editable = ['stock', 'outstanding']
    fields = ('description', 'sku_code', 'stock', 'category', 'type', 'size','cant', 'colors','l', 'h', 'v', 'cubic_meter', 'price_before_taxes', 'freight', 'custom_taxe', 'price', 'sale_price', 'discount_price', 'margin', 'gain', 'image', 'image_1', 'image_2', 'image_3', 'image_4', 'video_item',)

    readonly_fields = ('cubic_meter', 'price', 'slug', 'gain',)
    list_per_page = 10

    list_filter = [
        'outstanding',
        'category',
        'type',
        'size',
        'cant',
        'colors',
    ]

    def imageProduct(self, obj):
        return format_html('<img src="{}" width="130"/>', obj.image.url)
    imageProduct.short_description = 'Imagen'


class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_order_subtotal',
        'get_order_iva',
        'get_order_total',
        'payment_method',
        'status',
        'ordered',
        'ordered_date',
    )
    readonly_fields = [
        'user',
        'promoCode',
        'items',
        'start_date',
        'ordered_date',
        'ordered',
        'payment_method',
        'status',
        'message',
        'billing_address',
        'shipping_address',
        'get_total_order',
        'image',
    ]

    list_filter = [
        'ordered',
        'promoCode',
        'payment_method',
        'status'
    ]

    def get_order_subtotal(self, obj):
        return obj.get_total()
    get_order_subtotal.short_description = 'Subtotal'

    def get_order_iva(self, obj):
        return obj.get_iva_order()
    get_order_iva.short_description = 'IVA'

    def get_order_total(self, obj):
        return obj.get_total_order()
    get_order_total.short_description = 'Total'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'get_item_sku',
        'get_item_name',
        'user',
        'quantity',
        'totalItem',
        'ordered',
    )
    readonly_fields = ['user',
                       'ordered',
                       'item',
                       'color',
                       'cant',
                       'quantity',
                       'totalItem', ]

    list_filter = [
        'ordered'
    ]

    def get_item_name(self, obj):
        return obj.item.description
    get_item_name.short_description = 'Item'

    def get_item_sku(self, obj):
        return obj.item.sku_code
    get_item_sku.short_description = 'Código SKU'


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    )

    fields = [
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    ]

    readonly_fields = [
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    ]


class BillingAddressadmin(admin.ModelAdmin):
    list_display = (
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    )
    fields = [
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    ]

    readonly_fields = [
        'user',
        'direction',
        'CodeLocation',
        'Province',
        'district',
    ]


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = (
        'username',
        'first_name',
        'last_name',
        'doc',
        'phone',
        'email',
        'is_superuser',
    )

    fields = [
        'username',
        'last_login',
        'is_superuser',
        'first_name',
        'last_name',
        'doc',
        'phone',
        'email',
        'date_joined',
    ]

    readonly_fields = [
        'username',
        'last_login',
        # 'is_superuser',
        'first_name',
        'last_name',
        'doc',
        'phone',
        'email',
        'date_joined',
    ]
    list_per_page = 10

    list_filter = [
        'is_superuser'
    ]



admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BillingAddress, BillingAddressadmin)
# admin.site.register(ColorItem, ColorItemAdmin)
# admin.site.register(CantItem, CantItemAdmin)

admin.site.site_header = 'Admin Cositas favoritas'
admin.site.index_title = 'Panel de control Cositas favoritas'
admin.site.site_title = 'Cositas favoritas'

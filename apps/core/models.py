from cProfile import label
from pyexpat import model
from statistics import mode
from turtle import title
from django.db import models
from django.conf import settings
from django.forms import NullBooleanField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField
from django.shortcuts import reverse

import random
# Create your models here.

CATEGORY_CHOICES = (
        ('A', '1-3 Años'),
        ('B', 'Bebés'), 
        ('C', '3 Años en Adelante'),
        ('D', 'Otros'), 
    )


STATUS_CHOICES = (
        ('P', 'PAYPAL'),
        ('TB', 'TRANSFERENCIA BANCARIA'),
        ('CA', 'EFECTIVO'),
    )

class User(AbstractUser):
    phone = models.CharField(max_length=12)
    doc = models.CharField(max_length=13, blank=True, null=True)
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

# PRODUCTOS
class Item(models.Model):
    sku_code = models.CharField(max_length=100, blank=False, null=False, verbose_name='Código SKU')
    description = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to = 'media', blank=False, null=False, verbose_name='Imagen Principal')
    image_1 = models.ImageField(upload_to = 'media', blank=True, null=True, verbose_name='Imagen 1',default='/media/transparent.png')
    image_2 = models.ImageField(upload_to = 'media', blank=True, null=True, verbose_name='Imagen 2',default='/media/transparent.png')
    image_3 = models.ImageField(upload_to = 'media', blank=True, null=True, verbose_name='Imagen 3',default='/media/transparent.png')
    image_4 = models.ImageField(upload_to = 'media', blank=True, null=True, verbose_name='Imagen 4',default='/media/transparent.png')
    stock = models.IntegerField(default=1, blank=False, null=False, verbose_name='Cantidad en stock')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, verbose_name='Categoría')
    discount_price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Precio de descuento')
    outstanding = models.BooleanField(default=False,blank=True, null=True, verbose_name='Destacados')
    
    video_item = EmbedVideoField(blank=True, null=True,verbose_name='Video del producto (Youtube)')
    
    # Dimensiones
    l = models.FloatField(blank=False, null=False)
    h = models.FloatField(blank=False, null=False)
    v = models.FloatField(blank=False, null=False,verbose_name='w')
    cubic_meter = models.CharField(max_length=100, blank=True, null=True, verbose_name='metro Cúbico')

    price_before_taxes = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2, verbose_name='Costo del producto')
    freight = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2, verbose_name='Flete')
    custom_taxe = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2, verbose_name='Impuestos aduanales')
    # costo total del producto:
    price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Costo total')
    # precio de venta:
    sale_price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Precio de venta')

    margin = models.CharField(max_length=100, blank=True, null=True, verbose_name='Margen')

    gain = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Ganancia')

    
    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        price = round((self.price_before_taxes) + (self.freight) + (self.custom_taxe),2)
        self.price = price
        self.gain = self.sale_price - price
        
        l = float(self.l)
        h = float(self.h)
        v = float(self.v)
        cubic = str((l/100 * h/100 * v/100))
        self.cubic_meter = cubic

        titulo = self.description
        titulo = titulo.strip()
        num = random.randint(1, 100)
        self.slug = slugify('product-{}-{}'.format(titulo, num))

        super(Item, self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('core:detailView', kwargs={
            'slug': self.slug
        })

    def get_iva_item(self):
        iva = round(float(self.sale_price ) * 0.07, 2)
        return iva

    def get_price_iva(self):
        iva = self.get_iva_item() + float(self.sale_price)
        return iva
    
    class Meta:
        verbose_name = "Tienda: Producto"
        verbose_name_plural = "Tienda: Productos"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    ordered = models.BooleanField(default=False, verbose_name='Pagado')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.IntegerField(default=1, verbose_name='cantidad')
    totalItem = models.DecimalField(null=True, blank=True,max_digits=100, decimal_places=2, verbose_name='Subtotal')

    def __str__(self):
        return f"{self.item.description} x{self.quantity} \n"

    def get_total_item_price(self):
        return self.quantity * self.totalItem
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

    def espaciado(self):
        return 149 - (len(self.item.description) + 1)
    
    def save(self, *args, **kwargs):
        self.totalItem = self.item.sale_price
        super(OrderItem, self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Producto Ordenado"
        verbose_name_plural = "Productos Ordenados"

class PromoCode(models.Model):
    promo_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Código de descuento')
    discount_total = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Descuento')

    def __str__(self):
        return self.promo_code
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='usuario')
    promoCode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name='Código de descuento')
    items = models.ManyToManyField(OrderItem, verbose_name='Productos')
    start_date = models.DateTimeField(auto_now_add= True, verbose_name='Fecha de inicio')
    ordered_date = models.DateTimeField(verbose_name='Fecha de pago')
    ordered = models.BooleanField(default=False, verbose_name='Pagado')
    payment_method = models.CharField(max_length=100, blank=True, null=True, choices=STATUS_CHOICES, verbose_name='Método de pago') 
    status = models.CharField(max_length=100, blank=True, null=True, verbose_name='Estatus')
    message = models.TextField(null=True, blank=True, verbose_name='Mensaje')
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Dirección de Facturación')
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Dirección de Compra')
    get_total_order = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2, verbose_name='Total de la orden')
    image = models.ImageField(upload_to = 'media', blank=False, null=False, verbose_name='Imagen')
    def __str__ (self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total +=round(float(order_item.get_final_price()), 2)
        total = round(float(total), 2)
        return total

    def get_iva_order(self):
        total = 0
        for order_item in self.items.all():
            total += round(float(order_item.get_final_price()), 2)
        total = round(float(total * 0.07), 2)
        return total
    
    def get_total_order(self):
        total = self.get_total() + self.get_iva_order()
        return total

    class Meta:
        verbose_name = "Tienda: Orden"
        verbose_name_plural = "Tienda: Ordenes"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Usuario')
    direction = models.CharField(max_length=100, verbose_name='Dirección')
    CodeLocation = models.CharField(max_length=100, verbose_name='Código Postal')
    Province = models.CharField(max_length=100, verbose_name='Provincia')
    district = models.CharField(max_length=100, verbose_name='Distrito')
    show = models.BooleanField(default=False, null=True)

    
    def __str__(self):
        return 'Dirección: ' + self.direction + ', Provincia: ' + self.Province

    class Meta:
        verbose_name = "Usuario: Dirección de envío"
        verbose_name_plural = 'Usuario: Direcciones de envío'

class BillingAddress(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    direction = models.CharField(max_length=100, verbose_name='Dirección')
    CodeLocation = models.CharField(max_length=100, verbose_name='Código Postal')
    Province = models.CharField(max_length=100, verbose_name='Provincia')
    district = models.CharField(max_length=100, verbose_name='Distrito')
    show = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return 'Dirección: ' + self.direction + ', Provincia: ' + self.Province
    
    class Meta:
        verbose_name = "Usuario: Dirección de facturación"
        verbose_name_plural = 'Usuario: Direcciones de facturación'


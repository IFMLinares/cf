from pyexpat import model
from turtle import title
from django.db import models
from django.conf import settings
from django.forms import NullBooleanField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
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
    sku_code = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to = 'media', blank=False, null=False)
    stock = models.IntegerField(default=1, blank=False, null=False)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    discount_price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)
    outstanding = models.BooleanField(default=False,blank=True, null=True)

    
    # Dimensiones
    l = models.FloatField(blank=False, null=False)
    h = models.FloatField(blank=False, null=False)
    v = models.FloatField(blank=False, null=False)
    cubic_meter = models.CharField(max_length=100, blank=True, null=True)

    price_before_taxes = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2)
    freight = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2)
    custom_taxe = models.DecimalField(blank=False, null=False,max_digits=100, decimal_places=2)
    # costo total del producto:
    price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)
    # precio de venta:
    sale_price = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)

    margin = models.CharField(max_length=100, blank=True, null=True)

    gain = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)

    def save(self, *args, **kwargs):
        price = round((self.price_before_taxes) + (self.freight) + (self.custom_taxe),2)
        self.price = price
        self.gain = self.sale_price - price
        
        l = int(self.l)
        h = int(self.h)
        v = int(self.v)
        cubic = l * h * v 
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalItem = models.DecimalField(null=True, blank=True,max_digits=100, decimal_places=2)

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
    promo_code = models.CharField(max_length=100, blank=True, null=True)
    discount_total = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promoCode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add= True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, blank=True, null=True, choices=STATUS_CHOICES) 
    status = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(null=True, blank=True)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    totalOrden = models.DecimalField(blank=True, null=True,max_digits=100, decimal_places=2)

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
                             on_delete=models.CASCADE)
    direction = models.CharField(max_length=100)
    CodeLocation = models.CharField(max_length=100)
    Province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    show = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Usuario: Dirección de envío"
        verbose_name_plural = 'Usuario: Direcciones de envío'

class BillingAddress(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    direction = models.CharField(max_length=100)
    CodeLocation = models.CharField(max_length=100)
    Province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    show = models.BooleanField(default=False, null=True)
    
    class Meta:
        verbose_name = "Usuario: Dirección de facturación"
        verbose_name_plural = 'Usuario: Direcciones de facturación'


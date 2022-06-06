from turtle import title
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
# Create your models here.

# PRODUCTOS
class Item(models.Model):
    sku_code = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to = 'media', blank=False, null=False)
    stock = models.IntegerField(default=1, blank=False, null=False)
    
    # Dimensiones
    l = models.CharField(max_length=100, blank=False, null=False)
    h = models.CharField(max_length=100, blank=False, null=False)
    v = models.CharField(max_length=100, blank=False, null=False)
    cubic_meter = models.CharField(max_length=100, blank=True, null=True)

    price_before_taxes = models.FloatField(blank=False, null=False)
    freight = models.FloatField(blank=False, null=False)
    custom_taxe = models.FloatField(blank=False, null=False)
    # costo total del producto:
    price = models.FloatField(blank=True, null=True)
    # precio de venta:
    sale_price = models.FloatField(blank=True, null=True)

    margin = models.CharField(max_length=100, blank=False, null=False)

    gain = models.CharField(max_length=100, blank=False, null=False)

    def save(self, *args, **kwargs):
        price = int(self.price_before_taxes) + int(self.freight) + int(self.custom_taxe)
        self.price = price
        self.gain = self.sale_price - price
        
        l = int(self.l)
        h = int(self.h)
        v = int(self.v)
        cubic = l * h * v 
        self.cubic_meter = cubic

        super(Item, self).save(*args,**kwargs)

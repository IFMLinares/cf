from turtle import title
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.shortcuts import reverse

import random
# Create your models here.

# PRODUCTOS
class Item(models.Model):
    sku_code = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to = 'media', blank=False, null=False)
    stock = models.IntegerField(default=1, blank=False, null=False)
    
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

    class Meta:
        verbose_name = "Tienda: Producto"
        verbose_name_plural = "Tienda: Productos"

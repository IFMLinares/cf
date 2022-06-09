from django.shortcuts import render

# django libraries

from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DeleteView, DetailView
from .models import Item
# Create your views here.

# Inicio de la pagima
class Index(TemplateView):
    template_name = 'index.html'

# Lista de Productos
class Store(ListView):
    model = Item
    paginate_by = 9
    template_name = 'store.html'
    context_object_name = 'items'

# Vista detalla del producto
class DetailView(DetailView):
    model = Item
    template_name = 'detail-view.html'
    context_object_name = 'item'

# Preguntas Frecuentes
class FAQView(TemplateView):
    template_name = 'faq.html'

# Carrito de compras
class cartView(TemplateView):
    template_name = 'cart.html'

# Checkout
class checkOutView(TemplateView):
    template_name = 'check-out.html'

# Orden Completa
class ordenCompletaView(TemplateView):
    template_name = 'ordenCompleta.html' 

# Cuenta de usuario
class miCuentaView(TemplateView):
    template_name = 'cuenta.html' 

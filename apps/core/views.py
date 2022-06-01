from django.shortcuts import render

# django libraries
from django.views.generic import TemplateView, ListView, DeleteView, DetailView

# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'

class Store(TemplateView):
    template_name = 'store.html'

class DetailView(TemplateView):
    template_name = 'detail-view.html'

class FAQView(TemplateView):
    template_name = 'faq.html'

class cartView(TemplateView):
    template_name = 'cart.html'

class checkOutView(TemplateView):
    template_name = 'check-out.html'

class ordenCompletaView(TemplateView):
    template_name = 'ordenCompleta.html' 

class miCuentaView(TemplateView):
    template_name = 'cuenta.html' 

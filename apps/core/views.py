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



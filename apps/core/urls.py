from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('product', DetailView.as_view(), name='detailView'),
    path('store', Store.as_view(), name='store'),
]

from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('product', DetailView.as_view(), name='detailView'),
    path('store', Store.as_view(), name='store'),
    path('faq', FAQView.as_view(), name='faq'),
    path('cart', cartView.as_view(), name='cart'),
    path('check-out', checkOutView.as_view(), name='check-out'),
    path('checkout-completa', ordenCompletaView.as_view(), name='checkoutCompleta'),
<<<<<<< HEAD
=======
    path('cuenta', miCuentaView.as_view(), name='cuenta'),



>>>>>>> d0f61709dd91401470f642fec20b3d40c9de6862
]

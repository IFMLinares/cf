from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('product/<slug>', DetailView.as_view(), name='detailView'),
    path('store/', Store.as_view(), name='store'),
    path('store/<category>', StoreFilter.as_view(), name='store_filter'),
    #camvios
    path('faq', FAQView.as_view(), name='faq'),
    path('cart', cartView.as_view(), name='cart'),
    path('check-out', checkOutView.as_view(), name='check-out'),
    path('payment', PaymentView.as_view(), name='payment'),
    path('order-complete', paypal_return, name='CheckoutFinish'),
    path('account', miCuentaView.as_view(), name='account'),
    
    # FUNCIONES PARA EL CARRITO DE COMPRAS
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('addto/', addto, name='addto'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-cart-modal/<slug>/', remove_from_cart_modal, name='remove-from-cart-modal'),
    path('remove-single-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('paypal_return', paypal_return, name='paypal_return'),
    path('paypal_cancel', paypal_cancel, name='paypal_cancel'),
    path('UploadImagePayment', UploadImagePayment, name='updload_image'),
]

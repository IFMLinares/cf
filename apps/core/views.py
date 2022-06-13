from ast import Add
import random
from asyncio import constants
from django import views
from django.shortcuts import render

# django libraries
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, View
from pytz import country_names
from requests import request
from .models import Item, OrderItem, Order, Address
# Create your views here.

class CartMixin(ContextMixin):
  def get_order(self):
    if (self.request.user.is_authenticated):
        try:
            order = (Order.objects.get(user=self.request.user, ordered=False))
            if (order):
                return order
        except ObjectDoesNotExist:
            pass
    else:
        pass

  def get_context_data(self, **kwargs):
    ctx = super(CartMixin, self).get_context_data(**kwargs)
    ctx['carro'] = self.get_order()
    return ctx

# Inicio de la pagima
class Index(View):
    model = Item
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        try:
            items = list(Item.objects.filter(outstanding=True))
            context = {
            }
            if len(items) > 0 and len(items) >= 5 :
                items = random.sample(items,5)
                context['items'] = items
            elif len(items) > 0 and len(items)<5:
                items = random.sample(items,len(items))
                context['items'] = items
            if (self.request.user.is_authenticated):
                order = (Order.objects.get(user=self.request.user, ordered=False))
                if (order):
                    context['carro'] = order
                
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            return render(self.request, self.template_name)


# Lista de Productos
class Store(CartMixin,ListView):
    model = Item
    paginate_by = 9
    template_name = 'store.html'
    context_object_name = 'items'

# Vista detalla del producto
class DetailView(CartMixin, DetailView):
    model = Item
    template_name = 'detail-view.html'
    context_object_name = 'item'

# Preguntas Frecuentes
class FAQView(CartMixin, TemplateView):
    template_name = 'faq.html'

# Carrito de compras
class cartView(LoginRequiredMixin, View):
    model = Order
    template_name = 'cart.html'
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            items = Item.objects.all().only('slug')
            context = {
                'carro': order,
                'items': items
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna orden activa')
            return redirect('/')

# Checkout
class checkOutView(LoginRequiredMixin, CartMixin, View):
    model = Address
    template_name = 'check-out.html'
    def get(self, request, *args, **kwargs):
        # form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            address = list(Address.objects.filter(user=self.request.user))
            # user = User.objects.get(username=self.request.user.username)
            # form = CheckoutForm()
            context = {
                # 'form': form,
                'order': order,
                # 'address': address
                # 'user': user,
            }
            if(len(address)>= 1 ):
                context['addres'] = address
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.info(request, 'No tienes ninguna orden activa')
            return redirect('core:check-out')

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            # country = self.request.POST['country']
            # street_address = self.request.POST['street_address']
            # apartment_address = self.request.POST['apartment_address']
            # postal_code = self.request.POST['postal_code']
            save = self.request.POST['save']
            print(save)
            # method = self.request.POST['payment_method']

            # address = Address(
            #     user = self.request.user,
            #     street_address = street_address,
            #     apartment_address = apartment_address,
            #     postal_code = postal_code,
            #     country = country,
            #     # save = save
            # )
            
            # address.save()
            # order.billing_address = address
            # mount = order.get_total()
            # order.totalOrden = mount
            # order.ordered = True
            # order.save()
            # print(order.totalOrden)
            # print(mount)
            return redirect('core:cart')
        except ObjectDoesNotExist:
            return redirect('core:index')
# Orden Completa
class ordenCompletaView(LoginRequiredMixin, CartMixin,View):
    template_name = 'ordenCompleta.html' 

# Cuenta de usuario
class CheckoutFinish(LoginRequiredMixin, CartMixin,TemplateView):
    template_name = 'ordenCompleta.html' 

# Cuenta de usuario
class miCuentaView(LoginRequiredMixin, CartMixin,TemplateView):
    template_name = 'cuenta.html' 


# función de añadir al carro
@login_required
def addto(request):
    if request.method=='POST':
        slug = request.POST['slug']
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # verificando si el item odernado ya está en la orden
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, 'La cantidad de este producto fue actualizada satisfactoriamente')
                return redirect('core:store')
            else:
                order.items.add(order_item)
                messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
                return redirect('core:store')
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
        return redirect('core:store')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'La cantidad de este producto fue actualizada satisfactoriamente')
            return redirect('core:cart')

# función para restar 1 del carrito
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save() 
            else:
                return redirect('core:remove-from-cart', slug=slug)
        else:
            messages.info(request, 'Este producto no está en su carrito')
            return redirect('core:cart')
    else:
        messages.info(request, 'Justo ahora no tienes ninguna orden activa')
        return redirect('core:cart')

    return redirect('core:cart')

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Este Producto fue eliminado satisfactoriamente')
            return redirect('core:cart')
        else:
            messages.info(request, 'Este producto no está en su carrito')
            return redirect('core:cart', slug=slug)
    else:
        messages.info(request, 'Justo ahora no tienes ninguna orden activa')
        return redirect('core:cart', slug=slug)

@login_required
def remove_from_cart_modal(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Este Producto fue eliminado satisfactoriamente')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.info(request, 'Este producto no está en su carrito')
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, 'Justo ahora no tienes ninguna orden activa')
        return redirect(request.META['HTTP_REFERER'])

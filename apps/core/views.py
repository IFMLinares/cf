import re
from urllib import response
import uuid
import zeep
from datetime import datetime
import random
from ast import Add
from asyncio import constants
from django import dispatch, views
from django.shortcuts import render
from django.conf import settings
# django libraries
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, View
from pytz import country_names
from requests import request
from paypal.standard.forms import PayPalPaymentsForm
from .models import Item, OrderItem, Order, Address, BillingAddress,User
from .forms.forms import CheckoutForm, CheckoutForm1
from .decoratorsp.decorators import login_required_message
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
            if self.request.user.is_authenticated:
                order = (Order.objects.get(user=self.request.user, ordered=False))
                context['items'] = items
                context['carro'] = order

            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {
            }
            if len(items) > 0 and len(items) >= 5 :
                items = random.sample(items,5)
                context['items'] = items
            elif len(items) > 0 and len(items)<5:
                items = random.sample(items,len(items))
                context['items'] = items
            return render(self.request, self.template_name,context)


# Lista de Productos
class Store(CartMixin,ListView):
    model = Item
    paginate_by = 9
    template_name = 'store.html'
    context_object_name = 'items'

    
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = 'alls'
        return context


class StoreFilter(CartMixin,ListView):
    model = Item
    paginate_by = 9
    template_name = 'store.html'
    context_object_name = 'items'
    
    def get_queryset(self, **kwars):
        return self.model.objects.filter(category=self.kwargs.get('category','alls'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category','alls')
        return context

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
                'order': order,
                'items': items
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna orden activa')
            return render(self.request, self.template_name)

# Checkout
class checkOutView(LoginRequiredMixin, CartMixin, View):
    model = Address
    template_name = 'check-out.html'
    def get(self, request, *args, **kwargs):
        # form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            address = list(Address.objects.filter(user=self.request.user))
            form = CheckoutForm()
            form1 = CheckoutForm1()
            context = {
                'carro': order,
                'order': order,
                'form': form,
                'form1': form1,
            }
            if(len(address)>= 1):
                context['addres'] = address
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.info(request, 'No tienes ninguna orden activa')
            return redirect('core:cart')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        form1 = CheckoutForm1(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                try:
                    direc = BillingAddress.objects.get(user=self.request.user)
                    direc.delete()
                except ObjectDoesNotExist:
                    pass

                try:
                    direc = Address.objects.get(user=self.request.user)
                    direc.delete()
                except ObjectDoesNotExist:
                    pass

                user = self.request.user
                direction = form.cleaned_data.get('directionforms')
                CodeLocation = form.cleaned_data.get('CodeLocation')
                Province = form.cleaned_data.get('Province')
                district = form.cleaned_data.get('district')
                show = form.cleaned_data.get('save')

                address = BillingAddress(
                    user = user,
                    direction = direction,
                    CodeLocation = CodeLocation,
                    Province = Province,
                    district = district,
                    show = show,
                )
                address.save()

                if(form.cleaned_data.get('same_shipping_address')):
                    shipping_Address = Address(
                        user = user,
                        direction = direction,
                        CodeLocation = CodeLocation,
                        Province = Province,
                        district = district,
                        show = show,
                    )
                else:
                    direction1 = self.request.POST.get('directionforms1')
                    CodeLocation1 = self.request.POST.get('CodeLocation1')
                    Province1 = self.request.POST.get('Province1')
                    district1 = self.request.POST.get('district1')
                    show1 = self.request.POST.get('save1')
                    if(show1 != True):
                        show1 = False
                    shipping_Address = Address(
                        user = user,
                        direction = direction1,
                        CodeLocation = CodeLocation1,
                        Province = Province1,
                        district = district1,
                        show = show1,
                    )
                
                shipping_Address.save()
                order.billing_address = address
                order.shipping_Address = shipping_Address

                mount = order.get_total_order()
                order.totalOrden = mount
                order.save()
                return redirect('core:payment')
            else:
                return redirect('core:index')
        except ObjectDoesNotExist:
            return redirect('core:index')

# Checkout
# @method_decorator(csrf_exempt, name=dispatch)
class PaymentView(LoginRequiredMixin, CartMixin, View):
    model = Address
    template_name = 'payment.html'


    def post(self, *args, **kwargs):
        address = BillingAddress.objects.get(user=self.request.user)
        order = Order.objects.get(user=self.request.user, ordered=False)
        order.ordered = True
        print(self.request.POST.get('payment_method'))
        payment_method = self.request.POST.get('payment_method')
        order.payment_method = payment_method
        order.status = 'En espera'
        numeroRuc =  ((20 - len(str(self.request.user.doc))) * '0') + str(self.request.user.doc)

        total = str(order.get_total())

        if total[-2] == '.':
            total = total + '0'
        totalIva = order.get_total_order()
        iva = order.get_iva_order()
        itemlist = []
        for item in order.items.all():
            item.ordered = True
            item.save()
            quantity = str(round(float(item.quantity),2) ) + '0'
            precioItem = item.item.sale_price
            precioItem2 = str(round(float(precioItem * item.quantity),2))
            if precioItem2[-2] == '.':
                precioItem2 = precioItem2 + '0'
            precioItemIVa = item.item.get_price_iva()
            precioIba = item.item.get_iva_item()
            itemsList ={
                "descripcion": 'Prueba',
                "cantidad": quantity,
                "precioUnitario": str(precioItem),
                "precioUnitarioDescuento": " ",
                "precioItem": str(precioItem2),
                "valorTotal": str(precioItemIVa),
                "tasaITBMS": "01",
                "valorITBMS": str(precioIba),
            }
            itemlist.append(itemsList)
        
        cliente = {
            "tipoClienteFE": "02",
            "tipoContribuyente": 1,
            "numeroRUC": numeroRuc,
            "pais": "PA",
            "correoElectronico1": self.request.user.email,
            "razonSocial": self.request.user.first_name + ' ' +self.request.user.last_name,
            # "direccion" : address.direction,
            # "CodigoUbicacion" : address.CodeLocation,
            "provincia" : address.Province,
            "distrito" : address.district,
            }
        

        # FACTURACIÓN THE FACTORYHKA
        numeroDocumentoFiscal =  int(((7 - len(str(order.pk))) * '0') + str(order.pk))
        wsdl = 'http://demoemision.thefactoryhka.com.pa/ws/obj/v1.0/Service.svc?singleWsdl'
        client = zeep.Client(wsdl=wsdl)
        datos = dict(
            tokenEmpresa="blzjnlwebrgp_tfhka",
            tokenPassword="d-$k;$4a$p++",
            documento=dict(
                codigoSucursalEmisor="0000",
                tipoSucursal="1",
                datosTransaccion=dict({
                    "tipoEmision": "01",
                    "tipoDocumento": "01",
                    "numeroDocumentoFiscal": str(numeroDocumentoFiscal),
                    "puntoFacturacionFiscal": "001",
                    "naturalezaOperacion": "01",
                    "tipoOperacion": 1,
                    "destinoOperacion": 1,
                    "formatoCAFE": 1,
                    "entregaCAFE": 1,
                    "envioContenedor": 1,
                    "procesoGeneracion": 1,
                    "tipoVenta": 1,
                    "fechaEmision": "2021-10-14T09:00:00-05:00",
                    "cliente": cliente
                }),
                listaItems=dict(
                    item=itemlist
                ),
                totalesSubTotales=dict({
                    "totalPrecioNeto": str(total),
                    "totalITBMS": str(iva),
                    "totalMontoGravado": str(iva),
                    "totalDescuento": "",
                    "totalAcarreoCobrado": "",
                    "valorSeguroCobrado": "",
                    "totalFactura": str(totalIva),
                    "totalValorRecibido": str(totalIva),
                    "vuelto": "0.00",
                    "tiempoPago": "1",
                    "nroItems": '1',
                    "totalTodosItems": str(totalIva),
                },
                listaFormaPago=dict(
                    formaPago=[
                        {"formaPagoFact": "02",
                        "descFormaPago": "",
                        "valorCuotaPagada": str(totalIva)},
                        ]
                    )
                )
            )
        )
        # res = (client.service.Enviar(**datos))
        # print(res)
        print(datos)
        order.save()
        context ={
            # 'res': res,
            'order': order
        }
        messages.success(self.request, 'Pago procesado exitosamente')
        return render(self.request, 'ordenCompleta.html', context)


    def get(self, request, *args, **kwargs):
        # form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': str(order.get_total_order()),
                'item_name': 'Order',
                'invoice': str(uuid.uuid4()),
                'currency_code': 'USD',
                'notify_url': f'http://{host}{reverse("paypal-ipn")}',
                'return_url': f'http://{host}{reverse("core:paypal_return")}',
                'cancel_return': f'http://{host}{reverse("core:paypal_cancel")}',
            }
            formPaypal = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                'order': order,
                'paypal': formPaypal,
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.info(request, 'No tienes ninguna orden activa')
            return redirect('core:cart')

# Orden Completa
class ordenCompletaView(LoginRequiredMixin, CartMixin,View):
    template_name = 'ordenCompleta.html' 

# Cuenta de usuario
class CheckoutFinish(LoginRequiredMixin, CartMixin,TemplateView):
    template_name = 'ordenCompleta.html' 

# Cuenta de usuario
class miCuentaView(LoginRequiredMixin, CartMixin, View):
    model = Order
    context_object_name = 'user'
    template_name = 'cuenta.html' 

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        try:
            orders_ordered = Order.objects.filter(user=self.request.user, ordered=True)
            orders_ordered = list(orders_ordered)
        except ObjectDoesNotExist:
            orders_ordered = ''
        try:
            user_billing_address = BillingAddress.objects.get(user=self.request.user)
            user_shipping_address = Address.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            user_billing_address = ''
            user_shipping_address = ''
        context = {
            'user': user,
            'orders': orders_ordered,
            'billing_address': user_billing_address,
            'shipping_address': user_shipping_address,
        }
        print(list((orders_ordered)))
        return render(self.request, self.template_name, context)

@login_required
@csrf_exempt
def paypal_return(request):
    try:
        address = BillingAddress.objects.get(user=request.user)
        order = Order.objects.get(user=request.user, ordered=False)
        order.ordered = True
        order.paymetn_metohd = 'P'
        order.status = 'PAGADO'

        total = str(order.get_total())
        print(total[-1])
        print(total[-2])
        if total[-2] == '.':
            total = total + '0'
        totalIva = order.get_total_order()
        iva = order.get_iva_order()
        itemlist = []
        for item in order.items.all():
            item.ordered = True
            item.save()
            quantity = str(round(float(item.quantity),2) ) + '0'
            precioItem = item.item.sale_price
            precioItem2 = str(round(float(precioItem * item.quantity),2))
            if precioItem2[-2] == '.':
                precioItem2 = precioItem2 + '0'
            precioItemIVa = item.item.get_price_iva()
            precioIba = item.item.get_iva_item()
            itemsList ={
                "descripcion": 'Prueba',
                "cantidad": quantity,
                "precioUnitario": str(precioItem),
                "precioUnitarioDescuento": " ",
                "precioItem": str(precioItem2),
                "valorTotal": str(precioItemIVa),
                "tasaITBMS": "01",
                "valorITBMS": str(precioIba),
            }
            itemlist.append(itemsList)
        
        cliente = {
            "tipoClienteFE": "02",
            "tipoContribuyente": 1,
            "numeroRUC": request.user.phone,
            "pais": "PA",
            "correoElectronico1": request.user.email,
            "razonSocial": request.user.first_name + ' ' +request.user.last_name,
            # "direccion" : address.direction,
            # "CodigoUbicacion" : address.CodeLocation,
            "provincia" : address.Province,
            "distrito" : address.district,
            }
        

        # FACTURACIÓN THE FACTORYHKA
        numeroDocumentoFiscal =  ((7 - len(str(order.pk))) * '0') + str(order.pk)
        wsdl = 'http://demoemision.thefactoryhka.com.pa/ws/obj/v1.0/Service.svc?singleWsdl'
        client = zeep.Client(wsdl=wsdl)
        datos = dict(
            tokenEmpresa="blzjnlwebrgp_tfhka",
            tokenPassword="d-$k;$4a$p++",
            documento=dict(
                codigoSucursalEmisor="0000",
                tipoSucursal="1",
                datosTransaccion=dict({
                    "tipoEmision": "01",
                    "tipoDocumento": "01",
                    "numeroDocumentoFiscal": str(numeroDocumentoFiscal),
                    "puntoFacturacionFiscal": "001",
                    "naturalezaOperacion": "01",
                    "tipoOperacion": 1,
                    "destinoOperacion": 1,
                    "formatoCAFE": 1,
                    "entregaCAFE": 1,
                    "envioContenedor": 1,
                    "procesoGeneracion": 1,
                    "tipoVenta": 1,
                    "fechaEmision": "2021-10-14T09:00:00-05:00",
                    "cliente": cliente
                }),
                listaItems=dict(
                    item=itemlist
                ),
                totalesSubTotales=dict({
                    "totalPrecioNeto": str(total),
                    "totalITBMS": str(iva),
                    "totalMontoGravado": str(iva),
                    "totalDescuento": "",
                    "totalAcarreoCobrado": "",
                    "valorSeguroCobrado": "",
                    "totalFactura": str(totalIva),
                    "totalValorRecibido": str(totalIva),
                    "vuelto": "0.00",
                    "tiempoPago": "1",
                    "nroItems": '1',
                    "totalTodosItems": str(totalIva),
                },
                listaFormaPago=dict(
                    formaPago=[
                        {"formaPagoFact": "02",
                        "descFormaPago": "",
                        "valorCuotaPagada": str(totalIva)},
                        ]
                    )
                )
            )
        )
        # res = (client.service.Enviar(**datos))
        # print(res)
        print(datos)
        order.save()
        context ={
            # 'res': res,
            'order': order
        }
        messages.success(request, 'Pago procesado exitosamente')
        return render(request, 'ordenCompleta.html', context)
        # return HttpResponse('ordenCompleta.html')
    except ObjectDoesNotExist:
        return redirect('core:cart')
    
@login_required
def paypal_cancel(request):
    messages.error(request, 'Pago Cancelado')
    return redirect('core:index')

# función de añadir al carro
@login_required_message(message='Debes iniciar sesión para completar está acción')
@login_required
def addto(request):
    if request.method=='POST':
        next = request.POST.get('next', '/store/')
        slug = request.POST['slug']
        item = get_object_or_404(Item, slug=slug)
        quantity = int(request.POST.get('quantity', 1))
        if request.user.is_authenticated:
            order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # verificando si el item odernado ya está en la orden
                if order.items.filter(item__slug=item.slug).exists():
                    order_item.quantity += quantity
                    order_item.save()
                    messages.info(request, 'La cantidad de este producto fue actualizada satisfactoriamente')
                    # return redirect('core:store')
                    return HttpResponseRedirect(next)
                else:
                    order_item.quantity = quantity
                    order_item.save()
                    order.items.add(order_item)
                    messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
                    # return redirect('core:store')
                    return HttpResponseRedirect(next)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
            # return redirect('core:store')
            return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/')

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

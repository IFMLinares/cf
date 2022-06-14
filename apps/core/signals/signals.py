from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from requests import request
from ..models import Order


@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn = sender
    if (ipn.payment_status == 'Completed'):
        print('valid')
        # print(ipn)
        # order = Order.objects.get(user=, ordered=False)
        # order.ordered = True
        # order.save()

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn = sender
    if (ipn.payment_status != 'Completed'):
        print('invalid')
        print(ipn)
        # order = Order.objects.get(user=request.user, ordered=False)
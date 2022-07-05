from django.shortcuts import render, get_object_or_404
from restaurant.models import Table, WaiterOrderPad
from collections import namedtuple

# Create your views here.
def client_table(request, slug):
    table = get_object_or_404(Table, slug=slug)
    Orders = namedtuple('Orders', ['ready', 'prepare', 'delivered'])
    orders = None

    try:
        waiter_order_pad = WaiterOrderPad.objects.get(table=table, status='open')
        ready_orders = waiter_order_pad.ordereditem_set.filter(status='ready')
        prepare_orders = waiter_order_pad.ordereditem_set.filter(status='prepare')
        delivered_orders = waiter_order_pad.ordereditem_set.filter(status='delivered')
        orders = Orders(
            ready_orders,
            prepare_orders,
            delivered_orders
        )
    except WaiterOrderPad.DoesNotExist:
        waiter_order_pad = None

    return render(
        request,
        'clients/client_table.html',
        locals()
    )

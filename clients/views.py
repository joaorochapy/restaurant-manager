from django.shortcuts import render, get_object_or_404
from restaurant.models import MenuItem, Table, WaiterOrderPad
from waiters.models import Task
from collections import namedtuple

from restaurant.models import Category
from django.db.models import Count, Q

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


def client_menu(request, slug):
    table = get_object_or_404(Table, slug=slug)
    categories = Category.objects.annotate(active=Count('menuitem',
                                           filter=Q(menuitem__active=True)))\
                                           .filter(active__gt=0)
    items_without_category = MenuItem.objects.filter(category__isnull=True, 
                                                     active=True)

    return render(request, 'clients/client_menu.html', locals())


def request_service(request, slug):
    table = get_object_or_404(Table, slug=slug)
    
    try:
        waiter_order_pad = WaiterOrderPad.objects.get(table=table,
                                                      status='open')
    except WaiterOrderPad.DoesNotExist:
        waiter_order_pad = None

    if waiter_order_pad:
        # Já existe comanda aberta na mesa que fez a solicitação.
        # Verifica se existe solicitação de atendimento pendente para a mesa,
        # exceto entrega.
        try:
            task = Task.objects.get(~Q(type='delivery'), table=table,
                                    status='pendding')

            if task.type != 'first_call':
                task.type = 'attendance'
                task.save()
        except Task.DoesNotExist:
            task = Task.objects.create(type='attendance', table=table)
    else:
        # Se não existir comanda aberta para a mesa.
        # Abre uma nova comanda para a mesa.
        waiter_order_pad = WaiterOrderPad.objects.create(table=table)
        # Cria uma nova tarefa de primeiro atendimento para a mesa.
        task = Task.objects.create(type='first_call', table=table)

    return render(request, 'clients/request.html', locals())


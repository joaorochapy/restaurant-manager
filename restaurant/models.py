from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Table(models.Model):
    number = models.CharField(verbose_name='Número',max_length=3, unique=True)
    slug = models.SlugField(verbose_name='Slug', max_length=8, blank=True,
                            unique=True)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesa'

    def __str__(self):
        return f'Mesa {self.number}'


    def save(self, *args, **kwargs):
        # Chamar metodo de criacao do slug
        self.slug_save()
        super(Table, self).save(*args, **kwargs)


    def slug_save(self):
        if not self.slug:
            self.slug = get_random_string(8)

            slug_is_wrong = True

            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(self).objects.filter(
                    slug=self.slug
                )

                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True

                if slug_is_wrong:
                    self.slug = get_random_string(8)


    def get_absolute_url(self):
        return reverse('client_table', args=[self.slug])


    def get_menu_url(self):
        return reverse('client_menu', args=[self.slug])


class WaiterOrderPad(models.Model):
    STATUS_OPTIONS = (
        ('open', 'Aberta'),
        ('close', 'Fechada'),
    )

    code = models.SlugField(verbose_name='Código', max_length=8, blank=True,
                            unique=True)
    table = models.ForeignKey(Table, verbose_name='Mesa', null=True,
                              on_delete=models.SET_NULL)
    openning = models.DateTimeField(verbose_name='Abertura', auto_now_add=True)
    closure = models.DateTimeField(verbose_name='Fechamento', blank=True,
                                   null=True)
    status = models.CharField(verbose_name='Status', max_length=7,
                              choices=STATUS_OPTIONS, default='aberta')
    amount = models.DecimalField(verbose_name='Valor total', max_digits=12,
                                 decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Comanda'
        verbose_name_plural = 'Comandas'

    def save(self, *args, **kwargs):
        # Creates and saves slug
        self.slug_save()
        super(WaiterOrderPad, self).save(*args, **kwargs)


    def slug_save(self):
        if not self.code:
            self.code = get_random_string(8)
            slug_is_wrong = True

            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(self).objects.filter(
                    code=self.code
                )

                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                if slug_is_wrong:
                    self.code = get_random_string(8)


    def update_amount(self):
        items = OrderedItem.objects.filter(waiter_order_pad=self)
        new_amount = 0.00

        for item in items:
            new_amount += float(item.price)

        self.amount = new_amount
        self.save()


    def __str__(self):
        return f'Comanda {self.code}'


class Category(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=55)
    description = models.TextField(verbose_name='Descrição', blank=True)
    order = models.IntegerField(verbose_name='Ordem', default=0, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('order', 'name')


    def __str__(self):
        return self.name


class MenuItem(models.Model):
    item = models.CharField(verbose_name='Item', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Categoria',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    price = models.DecimalField(verbose_name='Preço', max_digits=5,
                                decimal_places=2)
    active = models.BooleanField(verbose_name='Ativo?', default=True)
    need_to_prepare = models.BooleanField(verbose_name='Necessita de preparo?',
                                          default=True)
    description = models.TextField(verbose_name='Descrição', blank=True)

    class Meta:
        verbose_name = 'Item | Cardapio'
        verbose_name_plural = 'Itens | Cardapio'

    def __str__(self):
        return self.item


class OrderedItem(models.Model):
    STATUS_OPTIONS = (
        ('prepare', 'Em preparo'),
        ('ready', 'Pronto'),
        ('delivered', 'Entregue'),
    )

    item = models.ForeignKey(MenuItem, verbose_name='Item',
                             on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Preço',
                                max_digits=5, decimal_places=2)
    waiter_order_pad = models.ForeignKey(WaiterOrderPad,
                                         on_delete=models.PROTECT)
    status = models.CharField(verbose_name='Status', max_length=10,
                              choices=STATUS_OPTIONS, default='preparo')
    note = models.TextField(verbose_name='Nota', blank=True)
    order_time = models.DateTimeField(verbose_name='Hora do pedido',
                                      auto_now_add=True)
    delivery_time = models.DateTimeField(verbose_name='Hora da entrega',
                                         blank=True, null=True)

    class Meta:
        verbose_name = 'Item | Pedido'
        verbose_name_plural = 'Itens | Pedidos'
        ordering = ('order_time', 'item')


    def ready_order(self):
        if self.status == 'prepare':
            self.status = 'ready'
            self.save()


    def deliver_order(self):
        self.status = 'delivered'
        self.delivery_time = timezone.now()
        self.save()


    def __str__(self):
        return self.item.item

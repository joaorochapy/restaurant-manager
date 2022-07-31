from django.db import models
from django.conf import settings
from restaurant.models import Table
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    TYPE_OPTIONS = (
        ('first_call', 'Primeiro Atendimento'),
        ('attendance', 'Atendimento'),
        ('closure', 'Fechamento'),
        ('delivery', 'Entrega'),
    )

    STATUS_OPTIONS = (
        ('pending', 'Pendente'),
        ('concluded', 'Concluído'),
    )

    type = models.CharField(verbose_name='Tipo', max_length=16,
                            default='first_call', choices=TYPE_OPTIONS)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               verbose_name='Garçom', on_delete=models.PROTECT,
                               null=True, blank=True)
    status = models.CharField(max_length=9, choices=STATUS_OPTIONS,
                              default='pending')
    created_at = models.DateTimeField(verbose_name='Criada em',
                                      auto_now_add=True)
    attended_at = models.DateTimeField(verbose_name='atendida em',
                                       null=True, blank=True)
    table = models.ForeignKey(Table, verbose_name='Mesa', null=True,
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return f'{self.get_type_display()} na mesa {self.table.number}.'


    def meet_task(self, waiter):
        self.waiter = waiter
        self.status = 'concluded'
        self.attended_at = timezone.now()
        self.save()


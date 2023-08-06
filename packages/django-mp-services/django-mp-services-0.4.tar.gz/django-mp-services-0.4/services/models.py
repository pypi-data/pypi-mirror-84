
from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from basement.services import register_service
from services.managers import ServiceItemManager


class ServiceCategory(models.Model):

    name = models.CharField(_('Category name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service category')
        verbose_name_plural = _('Service categories')


class ServiceItem(models.Model):

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Category'))

    name = models.CharField(
        _('Service name'), max_length=255, blank=True, db_index=True)

    code = models.CharField(
        _('Code'), max_length=255, blank=True, db_index=True)

    price = models.FloatField(_('Price'))

    objects = ServiceItemManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('code', )
        verbose_name = _('Service item')
        verbose_name_plural = _('Service items')


class Service(models.Model):

    sale = models.ForeignKey(
        'invoices.Sale',
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Sale'),
        blank=True,
        null=True
    )

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Customer'),
        blank=True,
        null=True
    )

    item = models.ForeignKey(
        ServiceItem,
        on_delete=models.PROTECT,
        verbose_name=_('Service item')
    )

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    qty = models.IntegerField(_('Quantity'), default=1)

    price = models.FloatField(_('Price'))

    def __str__(self):
        if self.customer:
            return '{} - {}'.format(self.item.name, self.customer.name)

        return self.item.name

    def render(self):
        return render_to_string('services/item.html', {'object': self})

    @property
    def name(self):
        return self.item.name

    @property
    def code(self):
        return self.item.code

    @property
    def subtotal(self):
        return self.price * self.qty

    def set_qty(self, value):
        if self.qty != value:
            self.qty = value
            self.save(update_fields=['qty'])

    @property
    def set_qty_url(self):
        return reverse_lazy('services:set-qty', args=[self.pk])

    @property
    def remove_url(self):
        return reverse_lazy('services:remove', args=[self.pk])

    class Meta:
        db_table = 'services_service'
        verbose_name = _('Service')
        verbose_name_plural = _('Service')


class ServicesService(object):

    def __init__(self, invoices, user):
        self._user = user
        self._invoices = invoices
        self._check_access()

    def get_service(self, service_id):
        try:
            return Service.objects.get(pk=service_id)
        except ObjectDoesNotExist:
            raise Exception(_('Service not found'))

    def add_service(self, sale_id, service_item):

        sale = self._invoices.get_sale(sale_id)

        try:
            service = Service.objects.get(
                sale=sale,
                item=service_item
            )
            service.qty += 1
        except Service.DoesNotExist:
            service = Service(
                customer=sale.customer,
                sale=sale,
                item=service_item,
                price=service_item.price
            )

        service.save()

        return {
            'status': 'OK',
            'html': service.render(),
            'item_id': service.id,
            'total': sale.serialize_totals()
        }

    def set_service_qty(self, service_id, value):

        service = self.get_service(service_id)

        service.set_qty(value)

        return {'total': service.sale.serialize_totals()}

    def remove_service(self, service_id):

        service = self.get_service(service_id)

        sale = service.sale

        service.delete()

        return {'total': sale.serialize_totals()}

    def get_categories(self):
        return (
            ServiceCategory
                .objects
                .all()
                .prefetch_related('items')
        )

    def _check_access(self):
        if not self._user.is_staff:
            raise Exception(_('Access denied'))


@register_service('services')
def _construct_service(services, user, **kwargs):
    return ServicesService(services.invoices, user)

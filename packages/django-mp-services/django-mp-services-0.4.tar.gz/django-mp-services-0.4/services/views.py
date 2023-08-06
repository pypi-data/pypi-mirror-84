
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from basement.admin import admin_render_view
from basement.views import FilterView, FormActionView, ActionView

from services import forms
from services.models import ServiceItem, Service


@admin_render_view(template_name='services/print-service-items.html')
def print_service_items(request):
    return {}


@admin_render_view(template_name='services/print-services.html')
def print_services(request, sale_id):
    sale = request.env.invoices.get_sale(sale_id)
    return {
        'sale': sale,
        'services': sale.services.all()
    }


@admin_render_view(template_name='services/report.html')
def get_report(request):

    form = forms.ReportForm(request)

    services = Service.objects.filter(
        created__date__range=[
            form.cleaned_data['date_from'],
            form.cleaned_data['date_to']
        ]
    ).order_by('created')

    context = {
        'services': services,
        'form': form,
        'totals': {
            'qty': sum([s.qty for s in services]),
            'grand_total': sum([s.subtotal for s in services])
        }
    }

    context.update(form.cleaned_data)

    return context


get_service_items = FilterView(
    form_class=forms.SearchServiceForm,
    search_iterator=lambda request, url_kwargs, cleaned_data:
        ServiceItem.objects.search(**cleaned_data),
    items_template='services/service-items.html',
    decorators=[staff_member_required],
    per_page=30
)


add_service = FormActionView(
    message=_('Service added'),
    form_class=forms.ServiceItemSelectForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.services.add_service(
            service_item=cleaned_data['service_item'],
            **url_kwargs)
)


set_service_qty = FormActionView(
    message=_('Quantity changed'),
    form_class=forms.SetQtyForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.services.set_service_qty(
            value=cleaned_data['value'],
            **url_kwargs)
)


remove_service = ActionView(
    message=_('Service removed'),
    action=lambda request, url_kwargs, cleaned_data:
        request.env.services.remove_service(**url_kwargs)
)

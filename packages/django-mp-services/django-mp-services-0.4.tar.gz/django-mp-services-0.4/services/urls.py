
from django.urls import path

from services import views


app_name = 'services'


urlpatterns = [

    path('report/', views.get_report, name='report'),

    path('items/', views.get_service_items, name='items'),

    path('add-to-sale/<int:sale_id>/', views.add_service, name='add'),

    path('set-qty/<int:service_id>/', views.set_service_qty, name='set-qty'),

    path('remove/<int:service_id>/', views.remove_service, name='remove'),

    path('print-services/<int:sale_id>/', views.print_services,
         name='print-services'),

    path('print-service-items/', views.print_service_items,
         name='print-service-items')

]

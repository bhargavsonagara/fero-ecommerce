import django_filters
from django.db.models import Q

from drfapi.models import Order


def products_filter(queryset, name, value):
    """
        Allow coma seperated search too.
        ex: Product name are a1 and a2 then search a1, a2
        apply with OR statement.
    """

    value_filter_list = [x.strip() for x in value.split(',')]
    query_filters = Q()
    for vf in value_filter_list:
        query_filters |= Q(order_items__product__name__icontains=vf)
    return queryset.filter(query_filters)


def customers_filter(queryset, name, value):
    value_filter_list = [x.strip() for x in value.split(',')]
    query_filters = Q()
    for vf in value_filter_list:
        query_filters |= Q(customer__name__icontains=vf)
    return queryset.filter(query_filters)


class OrderFilterView(django_filters.FilterSet):
    """
        Filter of Order
    """

    products = django_filters.CharFilter(method=products_filter)
    customers = django_filters.CharFilter(method=customers_filter)

    class Meta:
        model = Order
        fields = ['products', 'customers']

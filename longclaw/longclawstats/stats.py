"""
Various stats/analysis calculations
"""
import itertools
import calendar
from datetime import datetime
from django.db.models import Q, Sum, F
from longclaw.longclaworders.models import Order, OrderItem


def current_month():
    now = datetime.now()
    n_days = calendar.monthrange(now.year, now.month)[1]
    month_start = datetime.strptime('1{}{}'.format(now.month, now.year), '%d%m%Y')
    month_end = datetime.strptime('{}{}{}'.format(n_days, now.month, now.year), '%d%m%Y')
    return month_start, month_end


def sales_for_time_period(from_date, to_date):
    """
    Get all sales for a given time period
    """
    sales = Order.objects.filter(
        Q(payment_date__lte=to_date) & Q(payment_date__gte=from_date)
    ).exclude(status=Order.CANCELLED)

    return sales


def daily_sales(from_date, to_date):
    sales = sales_for_time_period(from_date, to_date)
    grouped = itertools.groupby(sales, lambda order: order.payment_date.strftime("%Y-%m-%d"))
    return grouped

def sales_by_product(from_date, to_date):
    sales = OrderItem.objects.filter(
        Q(order__payment_date__lte=to_date) & Q(order__payment_date__gte=from_date)
    ).exclude(
        order__status=Order.CANCELLED
    ).annotate(
        title=F('product__product__title')
    ).values(
        'title'
    ).annotate(
        quantity=Sum('quantity')
    ).order_by('-quantity')

    return sales

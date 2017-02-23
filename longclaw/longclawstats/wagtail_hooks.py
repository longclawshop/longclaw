from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.site_summary import SummaryItem
from longclaw.longclaworders.models import Order
from longclaw.longclawproducts.models import Product
from longclaw.longclawstats import stats

class OutstandingOrdersSummary(SummaryItem):
    order = 10
    template = 'longclawhome/summary_item.html'
    def get_context(self):
        orders = Order.objects.filter(status=Order.SUBMITTED)
        return {
            'total': orders.count(),
            'text': 'Outstanding Orders',
            'url': '/admin/longclaworders/order/'
        }

class ProductCount(SummaryItem):
    order = 20
    template = 'longclawhome/summary_item.html'
    def get_context(self):
        return {
            'total': Product.objects.all().count(),
            'text': 'Products',
            'url': ''
        }

class MonthlySales(SummaryItem):
    order = 30
    template = 'longclawhome/summary_item.html'
    def get_context(self):
        sales = stats.sales_for_time_period(*stats.current_month())
        return {
            'total': sum(order.total for order in sales),
            'text': 'Sales this month',
            'url': '/admin/longclaworders/order/'
        }

@hooks.register('construct_homepage_summary_items')
def add_longclaw_summary_items(request, items):
    for item in items:
        items.remove(item)
    items.extend([
        OutstandingOrdersSummary(request),
        ProductCount(request),
        MonthlySales(request)
    ])

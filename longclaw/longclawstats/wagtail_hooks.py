import datetime
from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.site_summary import SummaryItem
from longclaw.longclaworders.models import Order
from longclaw.longclawstats import stats
from longclaw.longclawsettings.models import LongclawSettings
from longclaw.utils import ProductVariant, maybe_get_product_model


class LongclawSummaryItem(SummaryItem):
    order = 10
    template = 'longclawstats/summary_item.html'

    def get_context(self):
        return {
            'total': 0,
            'text': '',
            'url': '',
            'icon': 'icon-doc-empty-inverse'
        }

class OutstandingOrders(LongclawSummaryItem):
    order = 10
    def get_context(self):
        orders = Order.objects.filter(status=Order.SUBMITTED)
        return {
            'total': orders.count(),
            'text': 'Outstanding Orders',
            'url': '/admin/longclaworders/order/',
            'icon': 'icon-warning'
        }

class ProductCount(LongclawSummaryItem):
    order = 20
    def get_context(self):
        product_model = maybe_get_product_model()
        if product_model:
            count = product_model.objects.all().count()
        else:
            count = ProductVariant.objects.all().count()
        return {
            'total': count,
            'text': 'Product',
            'url': '',
            'icon': 'icon-list-ul'
        }

class MonthlySales(LongclawSummaryItem):
    order = 30
    def get_context(self):
        settings = LongclawSettings.for_site(self.request.site)
        sales = stats.sales_for_time_period(*stats.current_month())
        return {
            'total': "{}{}".format(settings.currency_html_code,
                                   sum(order.total for order in sales)),
            'text': 'In sales this month',
            'url': '/admin/longclaworders/order/',
            'icon': 'icon-tick'
        }

class LongclawStatsPanel(SummaryItem):
    order = 110
    template = 'longclawstats/stats_panel.html'
    def get_context(self):
        month_start, month_end = stats.current_month()
        daily_sales = stats.daily_sales(month_start, month_end)
        labels = [(month_start + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
                  for x in range(0, datetime.datetime.now().day)]
        daily_income = [0] * len(labels)
        for k, order_group in daily_sales:
            i = labels.index(k)
            daily_income[i] = float(sum(order.total for order in order_group))

        popular_products = stats.sales_by_product(month_start, month_end)[:5]
        return {
            "daily_income": daily_income,
            "labels": labels,
            "product_labels": list(popular_products.values_list('title', flat=True)),
            "sales_volume": list(popular_products.values_list('quantity', flat=True))
        }




@hooks.register('construct_homepage_summary_items')
def add_longclaw_summary_items(request, items):

    # We are going to replace everything with our own items
    items[:] = []
    items.extend([
        OutstandingOrders(request),
        ProductCount(request),
        MonthlySales(request)
    ])

@hooks.register('construct_homepage_panels')
def add_stats_panel(request, panels):
    return panels.append(LongclawStatsPanel(request))

from django.views.generic import ListView
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket import utils

class BasketView(ListView):
    model = BasketItem
    template_name = "longclawbasket/basket.html"
    def get_context_data(self, **kwargs):
        items, _ = utils.get_basket_items(self.request)
        total_price = sum(item.total() for item in items)
        return {"basket": items, "total_price": total_price}

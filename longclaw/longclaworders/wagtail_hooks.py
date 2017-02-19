from django.contrib.admin.utils import quote
from django.utils.translation import ugettext as _
from django.conf.urls import url
from rest_framework.renderers import JSONRenderer

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.views import InspectView
from longclaw.longclaworders.models import Order
from longclaw.longclaworders.serializers import OrderSerializer

class OrderButtonHelper(ButtonHelper):

    detail_button_classnames = []
    cancel_button_classnames = ['no']

    def cancel_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = ['cancel-button']
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.cancel_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': '',
            'label': _('Cancel'),
            'classname': cn,
            'title': _('Cancel this %s') % self.verbose_name,
        }

    def detail_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = ['detail-button']
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.detail_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url('detail', quote(pk)),
            'label': _('View'),
            'classname': cn,
            'title': _('View this %s') % self.verbose_name,
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        if exclude is None:
            exclude = []
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        ph = self.permission_helper
        usr = self.request.user
        pk = quote(getattr(obj, self.opts.pk.attname))
        btns = []
        if ph.user_can_inspect_obj(usr, obj):
            btns.append(self.detail_button(
                pk, classnames_add, classnames_exclude))
            btns.append(self.cancel_button(
                pk, classnames_add, classnames_exclude))

        return btns


class DetailView(InspectView):

    def get_page_title(self, **kwargs):
        return "Order #{}".format(self.instance.id)

    def get_page_subtitle(self, **kwargs):
        return ''

    def get_context_data(self, **kwargs):
        context = {
            'order_id': self.instance.id
        }
        context.update(kwargs)
        return super(DetailView, self).get_context_data(**context)

    def get_template_names(self):
        return 'orders_detail.html'


class OrderModelAdmin(ModelAdmin):
    model = Order
    menu_order = 100
    menu_icon = 'list-ul'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('id', 'status', 'status_note', 'email',
                    'payment_date', 'total_items', 'total')
    list_filter = ('status', 'payment_date', 'email')
    inspect_view_enabled = True
    detail_view_class = DetailView
    button_helper_class = OrderButtonHelper

    def detail_view(self, request, instance_pk):
        """
        Instantiates a class-based view to provide 'inspect' functionality for
        the assigned model. The view class used can be overridden by changing
        the 'inspect_view_class' attribute.
        """
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.detail_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        """
        Utilised by Wagtail's 'register_admin_urls' hook to register urls for
        our the views that class offers.
        """
        urls = super(OrderModelAdmin, self).get_admin_urls_for_registration()
        urls = urls + (
            url(self.url_helper.get_action_url_pattern('detail'),
                self.detail_view,
                name=self.url_helper.get_action_url_name('detail')),
        )
        return urls

modeladmin_register(OrderModelAdmin)

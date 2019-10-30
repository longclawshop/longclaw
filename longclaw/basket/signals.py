import django.dispatch

basket_modified = django.dispatch.Signal(providing_args=['basket_id'])

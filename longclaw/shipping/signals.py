import django.dispatch

address_modified = django.dispatch.Signal(providing_args=['instance'])

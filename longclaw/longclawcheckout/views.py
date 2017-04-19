from django.shortcuts import render
from django.views.generic.edit import FormView

# Create your views here.
class CheckoutView(FormView):
    template_name = "longclawcheckout/checkout.html"

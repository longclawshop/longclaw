import braintree
from longclaw import settings
from longclaw.longclawsettings.models import LongclawSettings
from longclaw.longclawcheckout.errors import PaymentError
from longclaw.longclawcheckout.gateways import BasePayment

class BraintreePayment(BasePayment):
    '''
    Create a payment using Braintree
    '''
    def __init__(self):
        if settings.BRAINTREE_SANDBOX:
            env = braintree.Environment.Sandbox
        else:
            env = braintree.Environment.Production
        braintree.Configuration.configure(env,
                                          merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                          public_key=settings.BRAINTREE_PUBLIC_KEY,
                                          private_key=settings.BRAINTREE_PRIVATE_KEY)

    def create_payment(self, request, amount, description=''):
        nonce = request.POST.get('payment_method_nonce')
        result = braintree.Transaction.sale({
            "amount": str(amount),
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if not result.is_success:
            raise PaymentError(result)
        return result.transaction.id

    def get_token(self, request=None):
        # Generate client token
        return braintree.ClientToken.generate()

    def client_js(self):
        return (
            "https://js.braintreegateway.com/web/dropin/1.2.0/js/dropin.min.js",
            "https://js.braintreegateway.com/web/3.15.0/js/client.min.js",
            "https://js.braintreegateway.com/web/3.15.0/js/hosted-fields.min.js"
        )

class PaypalVZeroPayment(BasePayment):
    '''
    Create a payment using the Paypal/Braintree v.zero SDK
    '''
    def __init__(self):
        self.gateway = braintree.BraintreeGateway(access_token=settings.VZERO_ACCESS_TOKEN)

    def create_payment(self, request, amount, description=''):
        longclaw_settings = LongclawSettings.for_site(request.site)
        nonce = request.POST.get('payment_method_nonce')
        result = self.gateway.transaction.sale({
            "amount": str(amount),
            "payment_method_nonce": nonce,
            "merchant_account_id": longclaw_settings.currency,
            "options": {
                "paypal": {
                    "description": description
                }
            }
        })
        if not result.is_success:
            raise PaymentError(result.message)
        return result.transaction.order_id

    def get_token(self, request):
        return self.gateway.client_token.generate()

    def client_js(self):
        return (
            "https://www.paypalobjects.com/api/checkout.js",
            "https://js.braintreegateway.com/web/3.15.0/js/client.min.js",
            "https://js.braintreegateway.com/web/3.15.0/js/paypal-checkout.min.js"
        )

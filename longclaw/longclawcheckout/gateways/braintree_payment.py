import braintree
from longclaw import settings
from longclaw.longclawsettings.models import LongclawSettings
from longclaw.longclawcheckout.utils import PaymentError
from longclaw.longclawcheckout.gateways import BasePayment

class BraintreePayment(BasePayment):
    '''
    Create a payment using Braintree
    '''
    def __init__(self):
        braintree.Configuration.configure(braintree.Environment.Sandbox,
                                          merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                          public_key=settings.BRAINTREE_PUBLIC_KEY,
                                          private_key=settings.BRAINTREE_PRIVATE_KEY)

    def create_payment(self, request, amount):
        nonce = request.data['payment_method_nonce']
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

    def get_token(self, request):
        # Generate client token for the dropin ui
        return braintree.ClientToken.generate({})

class PaypalVZeroPayment():
    '''
    Create a payment using the Paypal/Braintree v.zero SDK
    '''
    def __init__(self):
        self.gateway = braintree.BraintreeGateway(access_token=settings.VZERO_ACCESS_TOKEN)

    def create_payment(self, request, amount, description=''):
        longclaw_settings = LongclawSettings.for_site(request.site)
        nonce = request.data['payment_method_nonce']
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

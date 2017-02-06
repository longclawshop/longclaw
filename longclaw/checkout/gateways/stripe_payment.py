import math
import stripe
from longclaw.settings import CURRENCY, STRIPE_SECRET
from longclaw.checkout.utils import PaymentError
from longclaw.checkout.gateways import BasePayment


class StripePayment(BasePayment):
    '''
    Create a payment using stripe
    '''
    def __init__(self):
        stripe.api_key = STRIPE_SECRET

    def create_payment(self, request, amount):
        try:
            charge = stripe.Charge.create(
                amount=int(math.ceil(amount * 100)),  # Amount in pence
                currency=CURRENCY.lower(),
                source=request.data['token'],
                description="Payment from"
            )
        except stripe.error.CardError as error:
            raise PaymentError(error)

    def get_token(self, request):
        ''' Create a stripe token for a card
        '''
        return stripe.Token.create(
            card={
                "number": request.data["number"],
                "exp_month": request.data["exp_month"],
                "exp_year": request.data["exp_year"],
                "cvc": request.data["cvc"]

            }
        )

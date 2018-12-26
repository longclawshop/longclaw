from longclaw.checkout.errors import PaymentError

class BasePayment(object):
    """
    Provides the interface for payment backends and
    can function as a dummy backend for testing.
    """

    def create_payment(self, request, amount, description=''):
        """
        Dummy function for creating a payment through a payment gateway.
        Should be overridden in gateway implementations.
        Can be used for testing - to simulate a failed payment/error,
        pass `error: true` in the request data.
        """
        err = request.POST.get("error", False)
        if err:
            raise PaymentError("Dummy error requested")

        return 'fake_transaction_id'

    def get_token(self, request=None):
        """
        Dummy function for generating a client token through
        a payment gateway. Most (all?) gateways have a flow which
        involves requesting a token from the server to initialise
        a client.

        This function should be overriden in child classes
        """
        return 'dummy_token'

    def client_js(self):
        """
        Return any client javascript library paths required
        by the payment integration.
        Should return an iterable of JS paths which can
        be used in <script> tags
        """
        return ('http://dummy.js', 'dummy.js')

    def issue_refund(self, identifier, amount):
        """Issue a refund of the given amount.

        identifier is a id string to pass to the gateway
        in order to identify the transaction to refund.
        """
        assert isinstance(amount, (float, int))
        return True

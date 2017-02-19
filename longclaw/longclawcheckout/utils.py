
class PaymentError(Exception):    
    def __init__(self, message):
        self.message = str(message)

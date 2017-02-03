from django.db import models

class ShippingCountry(models.Model):
    ''' Standard and premimum rate shipping for
    individual countries.
    '''
    country_code = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=32)
    standard_rate = models.DecimalField(max_digits=12, decimal_places=2)
    standard_rate_carrier = models.CharField(max_length=64, default="Royal Mail")
    standard_rate_description = models.CharField(max_length=128,
                                                 default="Royal Mail standard shipping")
    premium_rate = models.DecimalField(max_digits=12, decimal_places=2)
    premium_rate_carrier = models.CharField(max_length=64, default="Royal Mail")
    premium_rate_description = models.CharField(max_length=128,
                                                default="Royal Mail tracked and signed for")


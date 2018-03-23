from rest_framework import serializers
from longclaw.contrib.productrequests.models import ProductRequest

class ProductRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRequest()
        fields = '__all__'

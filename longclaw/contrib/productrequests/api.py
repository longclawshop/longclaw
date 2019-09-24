from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from longclaw.contrib.productrequests.serializers import ProductRequestSerializer
from longclaw.contrib.productrequests.models import ProductRequest
from longclaw.utils import ProductVariant, maybe_get_product_model

class ProductRequestViewSet(viewsets.ModelViewSet):
    """create/list/get product requests
    """
    serializer_class = ProductRequestSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProductRequest.objects.all()

    def create(self, request):
        """Create a new product request
        """

        variant_id = request.data.get("variant_id", None)
        if variant_id is not None:
            variant = ProductVariant.objects.get(id=variant_id)
            product_request = ProductRequest(variant=variant)
            product_request.save()
            serializer = self.serializer_class(product_request)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                {"message": "Missing 'variant_id'"},
                status=status.HTTP_400_BAD_REQUEST)

        return response

    @action(detail=False, methods=['get'])
    def requests_for_variant(self, request, variant_id=None):
        """Get all the requests for a single variant
        """
        requests = ProductRequest.objects.filter(variant__id=variant_id)
        serializer = self.serializer_class(requests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

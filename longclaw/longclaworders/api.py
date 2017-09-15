from rest_framework.decorators import api_view
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from longclaw.longclaworders.models import Order
from longclaw.longclaworders.serializers import OrderSerializer


@api_view(["POST"])
def fulfill_order(request, pk):
    ''' Get all basket items
    '''
    order = Order.objects.get(id=pk)
    order.status = Order.FULFILLED
    order.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()

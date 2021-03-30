from rest_framework.decorators import action 
from rest_framework import permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from longclaw.orders.models import Order
from longclaw.orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        '=id', 'email', 
        'shipping_address__name', 'shipping_address__city',
    ]

    @action(detail=True, methods=['post'])
    def refund_order(self, request, pk):
        """Refund the order specified by the pk
        """
        order = Order.objects.get(id=pk)
        order.refund()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def fulfill_order(self, request, pk):
        """Mark the order specified by pk as fulfilled
        """
        order = Order.objects.get(id=pk)
        order.fulfill()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unfulfill_order(self, request, pk):
        """Unmark the order specified by pk as fulfilled
        """
        order = Order.objects.get(id=pk)
        order.unfulfill()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def order_statuses(self, request):
        return Response({value: text for value, text in Order.ORDER_STATUSES}, status=200)

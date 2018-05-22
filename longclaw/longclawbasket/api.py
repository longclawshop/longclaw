from rest_framework.decorators import detail_route, list_route
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket.serializers import BasketItemSerializer
from longclaw.longclawbasket import utils
from longclaw.utils import ProductVariant

class BasketViewSet(viewsets.ModelViewSet):
    """
    Viewset for interacting with a sessions 'basket' -
    ``ProductVariants`` which have been marked for checkout.BaseException
    """
    serializer_class = BasketItemSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self, request=None):
        items, _ = utils.get_basket_items(request or self.request)
        return items

    def create(self, request):
        """
        Add an item to the basket
        """
        variant_id = request.data.get("variant_id", None)

        if variant_id is not None:
            variant = ProductVariant.objects.get(id=variant_id)

            quantity = int(request.data.get("quantity", 1))
            items, bid = utils.get_basket_items(request)

            # Check if the variant is already in the basket
            in_basket = False
            for item in items:
                if item.variant.id == variant.id:
                    item.increase_quantity(quantity)
                    in_basket = True
                    break
            if not in_basket:
                item = BasketItem(variant=variant, quantity=quantity, basket_id=bid)
                item.save()

            serializer = BasketItemSerializer(self.get_queryset(request), many=True)
            response = Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)

        else:
            response = Response(
                {"message": "Missing 'variant_id'"},
                status=status.HTTP_400_BAD_REQUEST)

        return response

    def bulk_update(self, request):
        """Put multiple items in the basket,
        removing anything that already exists
        """
        # Delete everything in the basket
        bid = utils.destroy_basket(request)

        for item_data in request.data:
            item = BasketItem(basket_id=bid, **item_data)
            item.save()

        serializer = BasketItemSerializer(self.get_queryset(request), many=True)
        response = Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        return response

    def destroy(self, request, variant_id=None):
        """
        Remove an item from the basket
        """
        variant = ProductVariant.objects.get(id=variant_id)
        quantity = request.data.get("quantity", 1)
        try:
            item = BasketItem.objects.get(
                basket_id=utils.basket_id(request), variant=variant)
            item.decrease_quantity(quantity)
        except BasketItem.DoesNotExist:
            pass

        serializer = BasketItemSerializer(self.get_queryset(request), many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def total_items(self, request):
        """
        Get total number of items in the basket
        """
        n_total = 0
        for item in self.get_queryset(request):
            n_total += item.quantity

        return Response(data={"quantity": n_total}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def item_count(self, request, variant_id=None):
        """
        Get quantity of a single item in the basket
        """
        bid = utils.basket_id(request)
        item = ProductVariant.objects.get(id=variant_id)
        try:
            count = BasketItem.objects.get(basket_id=bid, variant=item).quantity
        except BasketItem.DoesNotExist:
            count = 0
        return Response(data={"quantity": count}, status=status.HTTP_200_OK)

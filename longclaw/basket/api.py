from django.apps import apps
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.basket.models import BasketItem
from longclaw.basket.serializers import BasketItemSerializer
from longclaw.basket import utils
from longclaw.basket.app_settings import PRODUCT_VARIANT_MODEL

ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_basket(request):
    ''' Get all basket items
    '''
    items, _ = utils.get_basket_items(request)
    serializer = BasketItemSerializer(items, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_item_count(request):
    '''
    Get quantity of a single item in the basket
    '''
    bid = utils.basket_id(request)
    item = ProductVariant.objects.get(id=request.GET["variant_id"])
    try:
        count = BasketItem.objects.get(basket_id=bid, product=item).quantity
    except BasketItem.DoesNotExist:
        count = 0
    return Response(data={"quantity": count}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def add_to_basket(request):
    '''
    Add an item to the basket
    '''
    variant = ProductVariant.objects.get(id=request.data["variant_id"])
    quantity = request.data.get("quantity", 1)

    items, bid = utils.get_basket_items(request)
    # Check if the variant is already in the basket
    in_basket = False
    for item in items:
        if item.product.id == variant.id:
            item.increase_quantity(quantity)
            in_basket = True
            break
    if not in_basket:
        item = BasketItem(product=variant, quantity=quantity, basket_id=bid)
        item.save()

    items, _ = utils.get_basket_items(request)
    serializer = BasketItemSerializer(items, many=True)
    return Response(data=serializer.data,
                    status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def remove_from_basket(request):
    '''
    Remove an item from the basket
    '''
    print(request.data["variant_id"])
    variant = ProductVariant.objects.get(id=request.data["variant_id"])
    quantity = request.data.get("quantity", 1)
    try:
        item = BasketItem.objects.get(basket_id=utils.basket_id(request), product=variant)
    except BasketItem.DoesNotExist:
        return Response(data={"message": "Item does not exist in cart"},
                        status=status.HTTP_400_BAD_REQUEST)

    if quantity >= item.quantity:
        item.delete()
    else:
        item.decrease_quantity(quantity)

    items, _ = utils.get_basket_items(request)
    serializer = BasketItemSerializer(items, many=True)
    return Response(data=serializer.data,
                    status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def basket_total_items(request):
    '''
    Get total number of items in the basket
    '''
    items, _ = utils.get_basket_items(request)
    n_total = 0
    for item in items:
        n_total += item.quantity

    return Response(data={"quantity": n_total}, status=status.HTTP_200_OK)

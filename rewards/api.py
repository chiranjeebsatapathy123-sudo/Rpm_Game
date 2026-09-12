from django.db import transaction

from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    ShopItem,
    InventoryItem,
    GoldTransaction,
    GoldTransactionType,
)


class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    item = ShopItemSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShopItem.objects.filter(active=True)
    serializer_class = ShopItemSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        item = self.get_object()
        user = request.user

        with transaction.atomic():
            character = user.character.__class__.objects.select_for_update().get(
                user=user
            )

            if InventoryItem.objects.filter(
                user=user,
                item=item
            ).exists():
                return Response(
                    {
                        "error": "You already own this item."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if character.gold < item.price:
                return Response(
                    {
                        "error": "Not enough Gold."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            character.gold -= item.price
            character.save(update_fields=['gold'])

            GoldTransaction.objects.create(
                user=user,
                amount=-item.price,
                transaction_type=GoldTransactionType.SPEND,
                shop_item=item,
                description=f"Purchased {item.name}"
            )

            inv_item = InventoryItem.objects.create(
                user=user,
                item=item
            )

        return Response(
            InventoryItemSerializer(inv_item).data,
            status=status.HTTP_201_CREATED
        )


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(
            user=self.request.user
        )

    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        inv_item = self.get_object()

        InventoryItem.objects.filter(
            user=request.user,
            item__item_type=inv_item.item.item_type
        ).update(
            equipped=False
        )

        inv_item.equipped = True
        inv_item.save(
            update_fields=['equipped']
        )

        return Response(
            {
                "success": True
            }
        )
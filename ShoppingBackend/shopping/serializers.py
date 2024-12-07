from rest_framework import serializers
from .models import Item, Cart, CartItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source='item',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'item', 'item_id', 'quantity', 'get_cost']
        read_only_fields = ['id', 'get_cost']

    def validate_quantity(self, value):
        """Ensure the quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        """Check if there is enough stock available for the item."""
        item = data['item']
        quantity = data['quantity']

        if item.stock < quantity:
            raise serializers.ValidationError(
                f"Not enough stock available for {item.name}. Only {item.stock} items left."
            )
        return data

    def create(self, validated_data):
        """Decrement item stock when added to cart."""
        item = validated_data['item']
        quantity = validated_data['quantity']

        # Deduct stock
        item.stock -= quantity
        item.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Adjust item stock when updating the cart item."""
        item = instance.item
        new_quantity = validated_data.get('quantity', instance.quantity)

        # Restore previous stock
        item.stock += instance.quantity

        # Deduct new quantity
        if item.stock < new_quantity:
            raise serializers.ValidationError(
                f"Not enough stock available for {item.name}. Only {item.stock} items left."
            )

        item.stock -= new_quantity
        item.save()

        instance.quantity = new_quantity
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        """Calculate the total cost of the cart, including tax and delivery fee."""
        return obj.calculate_total()

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, Cart, CartItem
from .serializers import ItemSerializer, CartSerializer, CartItemSerializer

# CRUD for Items
class ItemListCreateView(generics.ListCreateAPIView):
    """
    View to list all items and create a new item.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific item.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# Cart View
class CartView(APIView):
    def get_cart(self):
        """Retrieve the single cart or create it if it doesn't exist."""
        cart, created = Cart.objects.get_or_create(id=1)  # Fixed cart ID for simplicity
        return cart

    def get(self, request, *args, **kwargs):
        """Retrieve all items in the cart with calculated costs."""
        cart = self.get_cart()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Add an item to the cart or update its quantity."""
        cart = self.get_cart()
        data = request.data
        item_id = data.get('item_id')
        quantity = data.get('quantity', 1)

        if not item_id:
            return Response({"error": "Item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            return Response({"error": "Quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        # Ensure there's enough stock
        if item.stock < cart_item.quantity:
            return Response(
                {"error": f"Not enough stock for {item.name}. Available: {item.stock}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Adjust stock and save the cart item
        item.stock -= quantity
        item.save()
        cart_item.save()

        return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Remove one quantity of an item from the cart."""
        cart = self.get_cart()
        item_id = request.data.get('item_id')

        if not item_id:
            return Response({"error": "Item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        # Decrease the quantity by 1
        cart_item.quantity -= 1

        # Restore stock
        item = cart_item.item
        item.stock += 1
        item.save()

        # If quantity becomes zero, delete the CartItem
        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

        # Save updated cart item
        cart_item.save()
        return Response({"message": "One quantity removed from cart"}, status=status.HTTP_200_OK)

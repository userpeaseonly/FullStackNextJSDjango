from django.db import models
from decimal import Decimal
from users.models import CustomUser as User

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Inventory count
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)  # Path to store images
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        items = self.cartitem_set.all()
        subtotal = sum(Decimal(item.item.price) * item.quantity for item in items)
        tax = subtotal * Decimal('0.05')
        delivery_fee = Decimal('5.00') if subtotal < Decimal('60.00') else Decimal('0.00')
        total = subtotal + tax + delivery_fee
        return {
            'subtotal': subtotal,
            'tax': tax,
            'delivery_fee': delivery_fee,
            'total': total
        }

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart.user.username}'s cart"

    def get_cost(self):
        return self.item.price * self.quantity

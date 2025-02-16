from venv import logger

from django.db import models
from django.utils import timezone
from django.db import models
from users.models import User  # Assuming you have a custom User model
from products.models import Product  # Assuming you have a Product model

class Order(models.Model):
    ORDER_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING', choices=[
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def execute(self):
        """
        Execute the order and create a transaction.
        """
        if self.status != 'PENDING':
            raise ValueError("Order is not pending and cannot be executed.")

        # Find a matching order (e.g., a sell order for a buy order)
        opposite_type = 'SELL' if self.order_type == 'BUY' else 'BUY'
        matching_orders = Order.objects.filter(
            product=self.product,
            order_type=opposite_type,
            price=self.price,
            quantity=self.quantity,
            status='PENDING'
        )

        if matching_orders.exists():
            matching_order = matching_orders.first()

            # Create a transaction
            Transaction.objects.create(
                buyer=self.user if self.order_type == 'BUY' else matching_order.user,
                seller=matching_order.user if self.order_type == 'BUY' else self.user,
                product=self.product,
                quantity=self.quantity,
                price=self.price,
            )

            # Mark both orders as executed
            self.status = 'EXECUTED'
            matching_order.status = 'EXECUTED'
            self.save()
            matching_order.save()
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically execute the order.
        """
        super().save(*args, **kwargs)  # Save the order first
        if self.status == 'PENDING':  # Only execute if the order is pending
            self.execute()


class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_transactions')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_transactions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} - {self.product.name}"


class OrderBook(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_book')
    buy_orders = models.ManyToManyField(Order, related_name='buy_order_book')
    sell_orders = models.ManyToManyField(Order, related_name='sell_order_book')

    def __str__(self):
        return f"Order Book for {self.product.name}"
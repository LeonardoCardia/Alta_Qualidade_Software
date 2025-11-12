"""
Module for order processing and management.

This module provides functionality to process customer orders
with tier-based pricing.
"""

from legacy.price_calculator import PriceCalculator


class OrderService:
    """
    Service class for processing and managing customer orders.

    This class handles order creation, price calculation, and
    order summary generation for customers.
    """

    def __init__(self):
        """Initialize the OrderService with a PriceCalculator instance."""
        self.price_calculator = PriceCalculator()

    def process_order(self, client, items):
        """
        Process an order for a client with given items.

        Args:
            client (dict): A dictionary containing client information
                          with 'name' and 'tier' keys.
            items (list): A list of dictionaries, each containing
                         'name' and 'price' keys.

        Returns:
            dict: A dictionary containing order details with keys:
                  'client_name', 'tier', 'items', 'total', and 'discount'.
        """
        total = sum(item['price'] for item in items)
        discount_rate = self.price_calculator.get_discount_rate(client['tier'])
        final_total = self.price_calculator.calculate_price(
            total,
            client['tier']
        )

        order = {
            'client_name': client['name'],
            'tier': client['tier'],
            'items': items,
            'total': final_total,
            'discount': discount_rate
        }

        return order

    def generate_order_summary(self, order):
        """
        Generate a formatted summary of an order.

        Args:
            order (dict): A dictionary containing order information.

        Returns:
            str: A formatted string containing the order summary.
        """
        summary = f"Order for {order['client_name']} ({order['tier']} tier)\n"
        summary += "Items:\n"
        
        for item in order['items']:
            summary += f"  - {item['name']}: ${item['price']:.2f}\n"
        
        summary += f"Discount: {order['discount'] * 100:.0f}%\n"
        summary += f"Total: ${order['total']:.2f}\n"
        
        return summary

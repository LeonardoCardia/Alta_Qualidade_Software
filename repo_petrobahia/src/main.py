"""
Main application module for the PetroBahia order processing system.

This module serves as the entry point for the application, demonstrating
the usage of the order processing system with sample data.
"""

from legacy.clients import load_clients
from legacy.order_service import OrderService


def main():
    """
    Main function to demonstrate the order processing system.

    This function loads client data, creates sample orders,
    and displays order summaries.
    """
    # Load clients from file
    clients = load_clients('src/clients.txt')

    # Initialize order service
    order_service = OrderService()

    # Sample items for demonstration
    sample_items = [
        {'name': 'Product A', 'price': 100.0},
        {'name': 'Product B', 'price': 50.0},
        {'name': 'Product C', 'price': 75.0}
    ]

    # Process orders for each client
    print("=" * 60)
    print("PETROBAHIA - Order Processing System")
    print("=" * 60)
    print()

    for client in clients:
        order = order_service.process_order(client, sample_items)
        summary = order_service.generate_order_summary(order)
        print(summary)
        print("-" * 60)


if __name__ == '__main__':
    main()

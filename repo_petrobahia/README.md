# PetroBahia Order Processing System

A Python-based order processing system with tier-based pricing and discount management.

## Overview

This system provides a comprehensive solution for managing customer orders with automatic discount calculation based on client tier levels. It includes client data management, price calculation, and order processing capabilities.

## Features

- Client data management from text files
- Tier-based discount system (Gold, Silver, Bronze)
- Automated price calculation with discount application
- Order processing and summary generation
- PEP8 compliant codebase

## Project Structure

```
repo_petrobahia/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── clients.txt             # Client data file
│   └── legacy/
│       ├── clients.py          # Client data loader
│       ├── price_calculator.py # Price calculation logic
│       └── order_service.py    # Order processing service
├── clientes.txt                # Additional client data
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd repo_petrobahia
```

2. Ensure the client data file exists at `src/clients.txt`

## Usage

### Running the Application

```bash
python src/main.py
```

### Client Data Format

The client data file should follow this format:
```
Client Name, email@example.com, tier
```

Example:
```
John Doe, john@example.com, gold
Jane Smith, jane@example.com, silver
Bob Johnson, bob@example.com, bronze
```

### Tier Discount Rates

- Gold: 20% discount
- Silver: 10% discount
- Bronze: 5% discount

## Code Examples

### Loading Clients

```python
from legacy.clients import load_clients

clients = load_clients('src/clients.txt')
```

### Processing an Order

```python
from legacy.order_service import OrderService

order_service = OrderService()
items = [
    {'name': 'Product A', 'price': 100.0},
    {'name': 'Product B', 'price': 50.0}
]

order = order_service.process_order(client, items)
summary = order_service.generate_order_summary(order)
print(summary)
```

### Calculating Prices

```python
from legacy.price_calculator import PriceCalculator

calculator = PriceCalculator()
final_price = calculator.calculate_price(100.0, 'gold')  # Returns 80.0
```

## Development

### Code Standards

This project follows PEP8 Python coding standards:
- Maximum line length: 79 characters for code
- Proper docstrings for all modules, classes, and functions
- Consistent naming conventions
- Proper whitespace and indentation

### Testing

To verify the implementation:

```bash
python src/main.py
```

## Contributing

1. Create a feature branch from main
2. Follow PEP8 coding standards
3. Add appropriate documentation
4. Submit a pull request

## License

This project is proprietary software for PetroBahia internal use.

## Contact

For questions or support, please contact the development team.

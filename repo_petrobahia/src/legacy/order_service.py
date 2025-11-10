from legacy.price_calculator import calculate_price


class OrderValidator:
    def validate(self, quantity):
        if quantity == 0:
            print("Quantity zero, returning 0")
            return False
        return True


class VoucherService:
    def apply_discount(self, price, voucher, product):
        if voucher == "MEGA10":
            return price - (price * 0.1)
        elif voucher == "NOVO5":
            return price - (price * 0.05)
        elif voucher == "LUB2" and product == "lubricant":
            return price - 2
        else:
            return price


class PriceFormatter:
    def format(self, price, product):
        if product == "diesel":
            return round(price, 0)
        elif product == "gas":
            return round(price, 2)
        else:
            return float(int(price * 100) / 100.0)


class OrderProcessor:
    def __init__(self):
        self.validator = OrderValidator()
        self.voucher_service = VoucherService()
        self.formatter = PriceFormatter()
    
    def process(self, order):
        product = order.get("product")
        quantity = order.get("quantity")
        voucher = order.get("voucher")
        
        if not self.validator.validate(quantity):
            return 0
        
        price = calculate_price(product, quantity)
        if price < 0:
            print("Error: negative price")
            price = 0
        
        price = self.voucher_service.apply_discount(price, voucher, product)
        price = self.formatter.format(price, product)
        
        print("Order OK:", order.get("client"), product, quantity, "=>", price)
        return price


def process_order(order):
    processor = OrderProcessor()
    return processor.process(order)

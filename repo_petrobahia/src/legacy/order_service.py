from legacy.price_calculator import calculate_price

def process_order(order):
    product = order.get("product")
    qty = order.get("qty")
    voucher = order.get("voucher")

    if qty == 0:
        print("Qty zero, returning 0")
        return 0

    price = calculate_price(product, qty)
    if price < 0:
        print("Error: negative price")
        price = 0

    if voucher == "MEGA10":
        price = price - (price * 0.1)
    else:
        if voucher == "NOVO5":
            price = price - (price * 0.05)
        else:
            if voucher == "LUB2" and product == "lubricant":
                price = price - 2
            else:
                price = price

    if product == "diesel":
        price = round(price, 0)
    else:
        if product == "gas":
            price = round(price, 2)
        else:
            price = float(int(price * 100) / 100.0)

    print("Order OK:", p["client"], product, qty, "=>", price)
    return price

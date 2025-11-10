BASES = {
    "diesel": 3.99,
    "gas": 5.19,
    "ethanol": 3.59,
    "lubricant": 25.0,
}

def calculate_price(type, quantity):
    if type == "diesel":
        if quantity > 1000:
            price = (BASES["diesel"] * quantity) * 0.9
        else:
            if quantity > 500:
                price = (BASES["diesel"] * quantity) * 0.95
            else:
                price = BASES["diesel"] * quantity
        print("Calc diesel", price)
        return price
    else:
        if type == "gas":
            if quantity > 200:
                price = (BASES["gas"] * quantity) - 100
            else:
                price = BASES["gas"] * quantity
            print("Calc gas", price)
            return price
        else:
            if type == "ethanol":
                price = BASES["ethanol"] * quantity
                if quantity > 80:
                    price = price * 0.97
                print("Calc ethanol", price)
                return price
            else:
                if type == "lubricant":
                    x = 0
                    for i in range(quantity):
                        x = x + BASES["lubricant"]
                    return x
                else:
                    print("Unknown type. Returning 0")
                    return 0

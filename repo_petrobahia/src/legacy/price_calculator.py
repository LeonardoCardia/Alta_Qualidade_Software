BASES = {
    "diesel": 3.99,
    "gas": 5.19,
    "ethanol": 3.59,
    "lubricant": 25.0,
}


class PriceCalculator:
    def calculate(self, type, quantity):
        if type == "diesel":
            return self._calculate_diesel(quantity)
        elif type == "gas":
            return self._calculate_gas(quantity)
        elif type == "ethanol":
            return self._calculate_ethanol(quantity)
        elif type == "lubricant":
            return self._calculate_lubricant(quantity)
        else:
            print("Unknown type. Returning 0")
            return 0
    
    def _calculate_diesel(self, quantity):
        if quantity > 1000:
            price = (BASES["diesel"] * quantity) * 0.9
        elif quantity > 500:
            price = (BASES["diesel"] * quantity) * 0.95
        else:
            price = BASES["diesel"] * quantity
        print("Calc diesel", price)
        return price
    
    def _calculate_gas(self, quantity):
        if quantity > 200:
            price = (BASES["gas"] * quantity) - 100
        else:
            price = BASES["gas"] * quantity
        print("Calc gas", price)
        return price
    
    def _calculate_ethanol(self, quantity):
        price = BASES["ethanol"] * quantity
        if quantity > 80:
            price = price * 0.97
        print("Calc ethanol", price)
        return price
    
    def _calculate_lubricant(self, quantity):
        x = 0
        for i in range(quantity):
            x = x + BASES["lubricant"]
        return x


def calculate_price(type, quantity):
    calculator = PriceCalculator()
    return calculator.calculate(type, quantity)

class PriceCalculator:
    """
    Um calculador para aplicar descontos baseados em níveis de cliente.

    Esta classe lida com cálculos de preços com diferentes taxas de desconto
    com base em níveis de cliente (ouro, prata, bronze).
    """

    DISCOUNT_RATES = {"gold": 0.20, "silver": 0.10, "bronze": 0.05}

    def calculate_price(self, base_price, tier):
        """
        Calcula o preço final após aplicar o desconto baseado no nível.

        Args:
            base_price (float): O preço original antes do desconto.
            tier (str): O nível do cliente ('gold', 'silver' ou 'bronze').

        Returns:
            float: O preço final após aplicar o desconto.

        Nota:
            Se o nível não for reconhecido, nenhum desconto será aplicado.
        """
        discount = self.DISCOUNT_RATES.get(tier.lower(), 0)
        final_price = base_price * (1 - discount)
        return final_price

    def get_discount_rate(self, tier):
        """
        Obtém a taxa de desconto para um nível específico.

        Args:
            tier (str): O nível do cliente.

        Returns:
            float: A taxa de desconto em formato decimal (por exemplo, 0,20 para 20%).
        """
        return self.DISCOUNT_RATES.get(tier.lower(), 0)

def calculate_total(items):
    """
    Soma preços de todos os itens da lista.
    Espera lista de dicionários com chave 'price'.
    """
    total = 0
    for item in items:
        total += item["price"]
    return total


def apply_tax(price):
    """Adiciona 10% de imposto ao preço."""
    return price * 1.10


def apply_discount(price, quantity):
    """
    Aplica desconto progressivo baseado em quantidade:
    - 10+ itens: 20% desconto
    - 5-9 itens: 10% desconto
    - <5 itens: sem desconto
    """
    if quantity >= 10:
        return price * 0.80
    if quantity >= 5:
        return price * 0.90
    return price


def calculate_final_price(items):
    """
    Calcula preço final: soma itens → aplica desconto por qtd → adiciona imposto.
    Retorna valor com 2 casas decimais.
    """
    total = calculate_total(items)
    quantity = len(items)
    total_with_discount = apply_discount(total, quantity)
    final_price = apply_tax(total_with_discount)
    return round(final_price, 2)

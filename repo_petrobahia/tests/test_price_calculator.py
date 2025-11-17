import pytest
from legacy.price_calculator import (
    PriceCalculator,
    calculate_total,
    apply_tax,
    apply_discount,
    calculate_final_price,
)

def test_price_calculator_tiers():
    calc = PriceCalculator()
    assert calc.calculate_price(100, "gold") == 80.0
    assert calc.calculate_price(100, "silver") == 90.0
    assert calc.calculate_price(100, "bronze") == 95.0
    assert calc.calculate_price(100, "unknown") == 100.0

def test_get_discount_rate():
    calc = PriceCalculator()
    assert calc.get_discount_rate("gold") == 0.20
    assert calc.get_discount_rate("silver") == 0.10
    assert calc.get_discount_rate("bronze") == 0.05
    assert calc.get_discount_rate("other") == 0

def test_calculate_total():
    items = [{"price": 10}, {"price": 20}, {"price": 5}]
    assert calculate_total(items) == 35

def test_apply_tax():
    assert apply_tax(100) == pytest.approx(110.0)

def test_apply_discount():
    assert apply_discount(100, 12) == 80.0  # 20% desconto
    assert apply_discount(100, 7) == 90.0   # 10% desconto
    assert apply_discount(100, 3) == 100.0  # sem desconto

def test_calculate_final_price():
    items = [{"price": 10}] * 12  # 12 itens, total 120, 20% desconto, +10% imposto
    assert calculate_final_price(items) == 105.6
    items = [{"price": 10}] * 7   # 7 itens, total 70, 10% desconto, +10% imposto
    assert calculate_final_price(items) == 69.3
    items = [{"price": 10}] * 3   # 3 itens, total 30, sem desconto, +10% imposto
    assert calculate_final_price(items) == 33.0
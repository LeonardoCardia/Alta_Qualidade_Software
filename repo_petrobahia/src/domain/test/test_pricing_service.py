from domain.entities.produto import TipoProduto
import pytest

from pathlib import Path

Path(
    
)

class TestPRICING_SERVICE():
    _BASE_PRICES = {
        TipoProduto.DIESEL: float("3.99"),
        TipoProduto.GASOLINA: float("5.19"),
        TipoProduto.ETANOL: float("3.59"),
        TipoProduto.LUBRIFICANTE: float("25.00"),
    }

    @pytest.mark.parametrize("tipo_produto", "quantidade", "expected_output",
                             [(TipoProduto.DIESEL, 5, 19.95),
                              (TipoProduto.GASOLINA, 10, 51.9),
                              (TipoProduto.ETANOL, 20, 71.8),
                              (TipoProduto.LUBRIFICANTE, -5, -125)])
    def test_calculate_price(self, tipo_produto: TipoProduto, quantidade: int, expected_output: float) -> float:
        

        base_price = self._BASE_PRICES.get(tipo_produto)
        if not base_price:
            raise ValueError(f"Unknown product type: {tipo_produto}")

        total = base_price * quantidade

        assert total == expected_output 
        # if tipo_produto == TipoProduto.DIESEL:
        #     return self._apply_diesel_discount(total, quantidade)
        # elif tipo_produto == TipoProduto.GASOLINA:
        #     return self._apply_gasolina_discount(total, quantidade)
        # elif tipo_produto == TipoProduto.ETANOL:
        #     return self._apply_etanol_discount(total, quantidade)

        #return total
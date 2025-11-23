import pytest
from domain.entities.produto import Produto, TipoProduto


class TestTipoProduto:

    def test_tipo_produto_diesel(self):
        assert TipoProduto.DIESEL.value == "diesel"

    def test_tipo_produto_gasolina(self):
        assert TipoProduto.GASOLINA.value == "gasolina"

    def test_tipo_produto_etanol(self):
        assert TipoProduto.ETANOL.value == "etanol"

    def test_tipo_produto_lubrificante(self):
        assert TipoProduto.LUBRIFICANTE.value == "lubrificante"

    def test_tipo_produto_enum_has_four_values(self):
        assert len(TipoProduto) == 4

    def test_tipo_produto_by_value(self):
        tipo = TipoProduto("diesel")
        assert tipo == TipoProduto.DIESEL


class TestProduto:

    def test_create_valid_produto_diesel(self):
        produto = Produto(tipo=TipoProduto.DIESEL, preco_base=3.99)
        assert produto.tipo == TipoProduto.DIESEL
        assert produto.preco_base == 3.99

    def test_create_valid_produto_gasolina(self):
        produto = Produto(tipo=TipoProduto.GASOLINA, preco_base=5.19)
        assert produto.tipo == TipoProduto.GASOLINA
        assert produto.preco_base == 5.19

    def test_create_valid_produto_etanol(self):
        produto = Produto(tipo=TipoProduto.ETANOL, preco_base=3.59)
        assert produto.tipo == TipoProduto.ETANOL
        assert produto.preco_base == 3.59

    def test_create_valid_produto_lubrificante(self):
        produto = Produto(tipo=TipoProduto.LUBRIFICANTE, preco_base=25.00)
        assert produto.tipo == TipoProduto.LUBRIFICANTE
        assert produto.preco_base == 25.00

    def test_produto_with_zero_price(self):
        produto = Produto(tipo=TipoProduto.DIESEL, preco_base=0.0)
        assert produto.preco_base == 0.0

    def test_produto_rejects_negative_price(self):
        with pytest.raises(ValueError, match="Product base price cannot be negative"):
            Produto(tipo=TipoProduto.DIESEL, preco_base=-1.0)

    def test_produto_rejects_negative_decimal_price(self):
        with pytest.raises(ValueError, match="Product base price cannot be negative"):
            Produto(tipo=TipoProduto.GASOLINA, preco_base=-0.01)

    def test_produto_with_high_precision_price(self):
        produto = Produto(tipo=TipoProduto.DIESEL, preco_base=3.99999)
        assert produto.preco_base == 3.99999

    def test_produto_with_large_price(self):
        produto = Produto(tipo=TipoProduto.LUBRIFICANTE, preco_base=1000.50)
        assert produto.preco_base == 1000.50

    def test_produto_is_immutable(self):
        produto = Produto(tipo=TipoProduto.DIESEL, preco_base=3.99)
        with pytest.raises(ValueError):
            produto.preco_base = 4.99

    @pytest.mark.parametrize("tipo,preco", [
        (TipoProduto.DIESEL, 3.99),
        (TipoProduto.GASOLINA, 5.19),
        (TipoProduto.ETANOL, 3.59),
        (TipoProduto.LUBRIFICANTE, 25.00),
    ])
    def test_produto_with_all_types_and_prices(self, tipo, preco):
        produto = Produto(tipo=tipo, preco_base=preco)
        assert produto.tipo == tipo
        assert produto.preco_base == preco

    @pytest.mark.parametrize("preco", [0.0, 0.01, 1.0, 10.0, 100.0, 1000.0])
    def test_produto_with_various_valid_prices(self, preco):
        produto = Produto(tipo=TipoProduto.DIESEL, preco_base=preco)
        assert produto.preco_base == preco

    @pytest.mark.parametrize("preco", [-0.01, -1.0, -10.0, -100.0])
    def test_produto_rejects_various_negative_prices(self, preco):
        with pytest.raises(ValueError, match="Product base price cannot be negative"):
            Produto(tipo=TipoProduto.DIESEL, preco_base=preco)

import pytest
from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto


class TestPedido:

    def test_create_valid_pedido_without_cupom(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )
        assert pedido.id == "pedido-001"
        assert pedido.cliente_id == "client-123"
        assert pedido.tipo_produto == TipoProduto.DIESEL
        assert pedido.quantidade == 100
        assert pedido.cupom is None

    def test_create_valid_pedido_with_cupom(self):
        pedido = Pedido(
            id="pedido-002",
            cliente_id="client-456",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=200,
            cupom="MEGA10"
        )
        assert pedido.cupom == "MEGA10"

    def test_pedido_validates_positive_quantidade(self):
        with pytest.raises(ValueError, match="Order quantity must be positive"):
            Pedido(
                id="pedido-003",
                cliente_id="client-789",
                tipo_produto=TipoProduto.ETANOL,
                quantidade=0
            )

    def test_pedido_rejects_negative_quantidade(self):
        with pytest.raises(ValueError, match="Order quantity must be positive"):
            Pedido(
                id="pedido-004",
                cliente_id="client-789",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=-10
            )

    def test_pedido_rejects_empty_id(self):
        with pytest.raises(ValueError, match="Order ID cannot be empty"):
            Pedido(
                id="",
                cliente_id="client-123",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=100
            )

    def test_pedido_rejects_empty_cliente_id(self):
        with pytest.raises(ValueError, match="Customer ID cannot be empty"):
            Pedido(
                id="pedido-005",
                cliente_id="",
                tipo_produto=TipoProduto.GASOLINA,
                quantidade=50
            )

    def test_pedido_with_quantidade_one(self):
        pedido = Pedido(
            id="pedido-006",
            cliente_id="client-123",
            tipo_produto=TipoProduto.LUBRIFICANTE,
            quantidade=1
        )
        assert pedido.quantidade == 1

    def test_pedido_with_large_quantidade(self):
        pedido = Pedido(
            id="pedido-007",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=10000
        )
        assert pedido.quantidade == 10000

    def test_pedido_strips_whitespace_from_id(self):
        pedido = Pedido(
            id="  pedido-008  ",
            cliente_id="client-123",
            tipo_produto=TipoProduto.ETANOL,
            quantidade=100
        )
        assert pedido.id == "pedido-008"

    def test_pedido_strips_whitespace_from_cliente_id(self):
        pedido = Pedido(
            id="pedido-009",
            cliente_id="  client-123  ",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )
        assert pedido.cliente_id == "client-123"

    def test_pedido_strips_whitespace_from_cupom(self):
        pedido = Pedido(
            id="pedido-010",
            cliente_id="client-123",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=100,
            cupom="  MEGA10  "
        )
        assert pedido.cupom == "MEGA10"

    def test_pedido_is_immutable(self):
        pedido = Pedido(
            id="pedido-011",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )
        with pytest.raises(ValueError):
            pedido.quantidade = 200

    @pytest.mark.parametrize("tipo_produto", [
        TipoProduto.DIESEL,
        TipoProduto.GASOLINA,
        TipoProduto.ETANOL,
        TipoProduto.LUBRIFICANTE,
    ])
    def test_pedido_with_all_product_types(self, tipo_produto):
        pedido = Pedido(
            id=f"pedido-{tipo_produto.value}",
            cliente_id="client-123",
            tipo_produto=tipo_produto,
            quantidade=50
        )
        assert pedido.tipo_produto == tipo_produto

    @pytest.mark.parametrize("quantidade", [1, 10, 100, 1000, 10000])
    def test_pedido_with_various_quantities(self, quantidade):
        pedido = Pedido(
            id="pedido-test",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=quantidade
        )
        assert pedido.quantidade == quantidade

    def test_pedido_cupom_optional(self):
        pedido_without = Pedido(
            id="pedido-012",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )
        pedido_with = Pedido(
            id="pedido-013",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100,
            cupom="NOVO5"
        )
        assert pedido_without.cupom is None
        assert pedido_with.cupom == "NOVO5"

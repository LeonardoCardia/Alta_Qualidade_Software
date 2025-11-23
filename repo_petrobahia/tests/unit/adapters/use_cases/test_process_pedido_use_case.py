import pytest
from unittest.mock import Mock
from adapters.use_cases.process_pedido_use_case import (
    ProcessPedidoUseCase,
    ProcessPedidoRequest,
    ProcessPedidoResponse
)
from domain.entities.pedido import Pedido
from domain.entities.cliente import Cliente
from domain.entities.produto import TipoProduto


class TestProcessPedidoUseCase:

    def setup_method(self):
        self.mock_pedido_repository = Mock()
        self.mock_cliente_repository = Mock()
        self.use_case = ProcessPedidoUseCase(
            self.mock_pedido_repository,
            self.mock_cliente_repository
        )

        self.valid_cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

    def test_execute_successful_order(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.message == "Order processed successfully"
        assert response.pedido is not None
        assert response.total is not None

    def test_execute_returns_pedido_and_total(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert isinstance(response.pedido, Pedido)
        assert isinstance(response.total, (int, float))

    def test_execute_handles_invalid_product_type(self):
        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="invalid_product",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert "Invalid product type" in response.message
        assert response.pedido is None
        assert response.total is None

    def test_execute_handles_customer_not_found(self):
        self.mock_cliente_repository.find_by_id.return_value = None

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="nonexistent",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert "Customer not found" in response.message

    def test_execute_handles_zero_quantity(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=0
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert "Quantity must be positive" in response.message

    def test_execute_handles_negative_quantity(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=-10
        )

        response = self.use_case.execute(request)

        assert response.success is False

    def test_execute_with_coupon(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100,
            cupom="MEGA10"
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.pedido.cupom == "MEGA10"

    def test_execute_calculates_correct_price(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        expected_price = 399.0
        assert response.total == expected_price

    def test_execute_handles_save_failure(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = False

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert response.message == "Failed to process order"

    @pytest.mark.parametrize("tipo_produto", [
        "diesel",
        "gasolina",
        "etanol",
        "lubrificante",
    ])
    def test_execute_with_all_product_types(self, tipo_produto):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=tipo_produto,
            quantidade=10
        )

        response = self.use_case.execute(request)

        assert response.success is True

    @pytest.mark.parametrize("invalid_tipo", [
        "invalid",
        "DIESEL",
        "Diesel",
        "",
        "gas",
    ])
    def test_execute_rejects_invalid_product_types(self, invalid_tipo):
        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=invalid_tipo,
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert response.success is False

    def test_execute_saves_pedido_to_repository(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        self.use_case.execute(request)

        self.mock_pedido_repository.save.assert_called_once()

    def test_execute_verifies_customer_exists(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        self.use_case.execute(request)

        self.mock_cliente_repository.find_by_id.assert_called_once_with("client-123")

    def test_response_structure_on_success(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert isinstance(response, ProcessPedidoResponse)
        assert hasattr(response, 'success')
        assert hasattr(response, 'message')
        assert hasattr(response, 'pedido')
        assert hasattr(response, 'total')

    def test_response_structure_on_failure(self):
        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="invalid",
            quantidade=100
        )

        response = self.use_case.execute(request)

        assert isinstance(response, ProcessPedidoResponse)
        assert response.success is False
        assert response.message is not None
        assert response.pedido is None
        assert response.total is None

    def test_execute_with_optional_cupom_none(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        request = ProcessPedidoRequest(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto="diesel",
            quantidade=100,
            cupom=None
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.pedido.cupom is None

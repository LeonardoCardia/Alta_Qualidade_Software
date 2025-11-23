import pytest
from unittest.mock import Mock
from adapters.use_cases.register_cliente_use_case import (
    RegisterClienteUseCase,
    RegisterClienteRequest,
    RegisterClienteResponse
)
from domain.entities.cliente import Cliente


class TestRegisterClienteUseCase:

    def setup_method(self):
        self.mock_repository = Mock()
        self.mock_notification = Mock()
        self.use_case = RegisterClienteUseCase(
            self.mock_repository,
            self.mock_notification
        )

    def test_execute_successful_registration(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.message == "Customer registered successfully"
        assert response.cliente is not None
        assert response.cliente.nome == "Empresa Teste"
        assert response.cliente.email == "contato@empresa.com"

    def test_execute_returns_cliente_in_response(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert isinstance(response.cliente, Cliente)

    def test_execute_handles_invalid_email(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="invalid-email",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert response.message == "Failed to register customer"
        assert response.cliente is None

    def test_execute_handles_invalid_cnpj(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="123"
        )

        response = self.use_case.execute(request)

        assert response.success is False
        assert response.cliente is None

    def test_execute_calls_repository_save(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.use_case.execute(request)

        self.mock_repository.save.assert_called_once()

    def test_execute_sends_notification(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.use_case.execute(request)

        self.mock_notification.send_welcome_email.assert_called_once()

    def test_execute_with_formatted_cnpj(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="12.345.678/9012-34"
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.cliente.cnpj == "12345678901234"

    def test_execute_with_whitespace_in_inputs(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="  Empresa Teste  ",
            email="  test@example.com  ",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert response.success is True
        assert response.cliente.nome == "Empresa Teste"
        assert response.cliente.email == "test@example.com"

    @pytest.mark.parametrize("invalid_email", [
        "plaintext",
        "@example.com",
        "user@",
        "user name@example.com",
    ])
    def test_execute_rejects_various_invalid_emails(self, invalid_email):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email=invalid_email,
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert response.success is False

    @pytest.mark.parametrize("invalid_cnpj", [
        "123",
        "1234567890123",
        "123456789012345",
        "12345678901ABC",
    ])
    def test_execute_rejects_various_invalid_cnpjs(self, invalid_cnpj):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj=invalid_cnpj
        )

        response = self.use_case.execute(request)

        assert response.success is False

    def test_response_structure_on_success(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="test@example.com",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert isinstance(response, RegisterClienteResponse)
        assert hasattr(response, 'success')
        assert hasattr(response, 'message')
        assert hasattr(response, 'cliente')

    def test_response_structure_on_failure(self):
        self.mock_repository.save.return_value = True

        request = RegisterClienteRequest(
            nome="Empresa",
            email="invalid",
            cnpj="12345678901234"
        )

        response = self.use_case.execute(request)

        assert isinstance(response, RegisterClienteResponse)
        assert response.success is False
        assert response.message is not None
        assert response.cliente is None

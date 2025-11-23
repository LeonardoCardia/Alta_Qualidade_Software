import pytest
from domain.entities.cliente import Cliente


class TestCliente:

    def test_create_valid_cliente(self):
        cliente = Cliente(
            nome="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )
        assert cliente.nome == "Empresa Teste"
        assert cliente.email == "contato@empresa.com"
        assert cliente.cnpj == "12345678901234"
        assert cliente.id is not None

    def test_cliente_generates_uuid(self):
        cliente = Cliente(
            nome="Empresa",
            email="test@company.com",
            cnpj="12345678901234"
        )
        assert len(cliente.id) > 0
        assert isinstance(cliente.id, str)

    def test_cliente_with_custom_id(self):
        cliente = Cliente(
            id="custom-id-123",
            nome="Empresa",
            email="test@company.com",
            cnpj="12345678901234"
        )
        assert cliente.id == "custom-id-123"

    def test_cliente_validates_email_format(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Cliente(
                nome="Empresa",
                email="invalid-email",
                cnpj="12345678901234"
            )

    def test_cliente_rejects_empty_email(self):
        with pytest.raises(ValueError, match="Email cannot be empty"):
            Cliente(
                nome="Empresa",
                email="",
                cnpj="12345678901234"
            )

    def test_cliente_validates_cnpj_length(self):
        with pytest.raises(ValueError, match="CNPJ deve conter 14 dígitos"):
            Cliente(
                nome="Empresa",
                email="test@company.com",
                cnpj="123456789"
            )

    def test_cliente_accepts_cnpj_with_formatting(self):
        cliente = Cliente(
            nome="Empresa",
            email="test@company.com",
            cnpj="12.345.678/9012-34"
        )
        assert cliente.cnpj == "12345678901234"

    def test_cliente_strips_whitespace_from_nome(self):
        cliente = Cliente(
            nome="  Empresa Teste  ",
            email="test@company.com",
            cnpj="12345678901234"
        )
        assert cliente.nome == "Empresa Teste"

    def test_cliente_strips_whitespace_from_email(self):
        cliente = Cliente(
            nome="Empresa",
            email="  test@company.com  ",
            cnpj="12345678901234"
        )
        assert cliente.email == "test@company.com"

    def test_cliente_is_immutable(self):
        cliente = Cliente(
            nome="Empresa",
            email="test@company.com",
            cnpj="12345678901234"
        )
        with pytest.raises(ValueError):
            cliente.nome = "Novo Nome"

    def test_cliente_with_valid_email_formats(self):
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
        ]
        for email in valid_emails:
            cliente = Cliente(
                nome="Empresa",
                email=email,
                cnpj="12345678901234"
            )
            assert cliente.email == email

    def test_cliente_cnpj_removes_special_characters(self):
        cliente = Cliente(
            nome="Empresa",
            email="test@company.com",
            cnpj="12.345.678/9012-34"
        )
        assert cliente.cnpj == "12345678901234"
        assert "." not in cliente.cnpj
        assert "/" not in cliente.cnpj
        assert "-" not in cliente.cnpj

    @pytest.mark.parametrize("invalid_email", [
        "plaintext",
        "@example.com",
        "user@",
        "user name@example.com",
    ])
    def test_cliente_rejects_invalid_emails(self, invalid_email):
        with pytest.raises(ValueError):
            Cliente(
                nome="Empresa",
                email=invalid_email,
                cnpj="12345678901234"
            )

    @pytest.mark.parametrize("invalid_cnpj", [
        "123",
        "1234567890123",
        "123456789012345",
        "12345678901ABC",
    ])
    def test_cliente_rejects_invalid_cnpjs(self, invalid_cnpj):
        with pytest.raises(ValueError):
            Cliente(
                nome="Empresa",
                email="test@company.com",
                cnpj=invalid_cnpj
            )

    def test_different_clientes_have_different_ids(self):
        cliente1 = Cliente(
            nome="Empresa 1",
            email="empresa1@test.com",
            cnpj="12345678901234"
        )
        cliente2 = Cliente(
            nome="Empresa 2",
            email="empresa2@test.com",
            cnpj="98765432109876"
        )
        assert cliente1.id != cliente2.id

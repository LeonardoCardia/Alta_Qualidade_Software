import pytest
from io import StringIO
import sys
from adapters.notifications.console_notification import ConsoleNotification
from domain.entities.cliente import Cliente


class TestConsoleNotification:

    def setup_method(self):
        self.notification = ConsoleNotification()
        self.cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

    def test_send_welcome_email_prints_message(self, capsys):
        self.notification.send_welcome_email(self.cliente)

        captured = capsys.readouterr()
        assert "[EMAIL]" in captured.out
        assert "Welcome message sent to" in captured.out
        assert "test@example.com" in captured.out

    def test_send_welcome_email_returns_true(self):
        result = self.notification.send_welcome_email(self.cliente)
        assert result is True

    def test_send_order_confirmation_prints_message(self, capsys):
        self.notification.send_order_confirmation(
            self.cliente,
            "pedido-001",
            "R$ 399.00"
        )

        captured = capsys.readouterr()
        assert "[EMAIL]" in captured.out
        assert "Order confirmation sent to" in captured.out
        assert "test@example.com" in captured.out
        assert "pedido-001" in captured.out
        assert "R$ 399.00" in captured.out

    def test_send_order_confirmation_returns_true(self):
        result = self.notification.send_order_confirmation(
            self.cliente,
            "pedido-001",
            "R$ 399.00"
        )
        assert result is True

    def test_send_welcome_email_with_different_clientes(self, capsys):
        cliente1 = Cliente(
            id="client-1",
            nome="Empresa 1",
            email="empresa1@test.com",
            cnpj="12345678901234"
        )

        cliente2 = Cliente(
            id="client-2",
            nome="Empresa 2",
            email="empresa2@test.com",
            cnpj="98765432109876"
        )

        self.notification.send_welcome_email(cliente1)
        self.notification.send_welcome_email(cliente2)

        captured = capsys.readouterr()
        assert "empresa1@test.com" in captured.out
        assert "empresa2@test.com" in captured.out

    def test_send_order_confirmation_with_order_number(self, capsys):
        self.notification.send_order_confirmation(
            self.cliente,
            "pedido-12345",
            "R$ 1,234.56"
        )

        captured = capsys.readouterr()
        assert "Order #pedido-12345" in captured.out

    def test_send_order_confirmation_with_total(self, capsys):
        self.notification.send_order_confirmation(
            self.cliente,
            "pedido-001",
            "R$ 999.99"
        )

        captured = capsys.readouterr()
        assert "Total: R$ 999.99" in captured.out

    def test_send_welcome_email_includes_email_tag(self, capsys):
        self.notification.send_welcome_email(self.cliente)

        captured = capsys.readouterr()
        assert captured.out.startswith("[EMAIL]")

    def test_send_order_confirmation_includes_email_tag(self, capsys):
        self.notification.send_order_confirmation(
            self.cliente,
            "pedido-001",
            "R$ 100.00"
        )

        captured = capsys.readouterr()
        assert captured.out.startswith("[EMAIL]")

    def test_send_welcome_email_with_special_characters_in_email(self, capsys):
        cliente = Cliente(
            id="client-123",
            nome="Empresa",
            email="user+tag@example.com",
            cnpj="12345678901234"
        )

        self.notification.send_welcome_email(cliente)

        captured = capsys.readouterr()
        assert "user+tag@example.com" in captured.out

    def test_send_order_confirmation_with_various_totals(self, capsys):
        test_totals = ["R$ 0.00", "R$ 10.50", "R$ 1,000,000.00"]

        for total in test_totals:
            self.notification.send_order_confirmation(
                self.cliente,
                "pedido-001",
                total
            )

            captured = capsys.readouterr()
            assert total in captured.out

    def test_send_welcome_email_output_format(self, capsys):
        self.notification.send_welcome_email(self.cliente)

        captured = capsys.readouterr()
        expected_format = f"[EMAIL] Welcome message sent to {self.cliente.email}"
        assert expected_format in captured.out

    def test_send_order_confirmation_output_format(self, capsys):
        order_id = "pedido-001"
        total = "R$ 399.00"

        self.notification.send_order_confirmation(
            self.cliente,
            order_id,
            total
        )

        captured = capsys.readouterr()
        assert f"Order #{order_id}" in captured.out
        assert f"Total: {total}" in captured.out

    def test_multiple_notifications_in_sequence(self, capsys):
        self.notification.send_welcome_email(self.cliente)
        self.notification.send_order_confirmation(
            self.cliente,
            "pedido-001",
            "R$ 100.00"
        )

        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')
        assert len(lines) == 2
        assert "Welcome message" in lines[0]
        assert "Order confirmation" in lines[1]

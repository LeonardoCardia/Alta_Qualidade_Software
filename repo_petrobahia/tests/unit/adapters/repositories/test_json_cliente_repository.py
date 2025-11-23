import pytest
import tempfile
import shutil
from pathlib import Path
from adapters.repositories.json_cliente_repository import JsonClienteRepository
from domain.entities.cliente import Cliente


class TestJsonClienteRepository:

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repository = JsonClienteRepository(data_dir=self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_repository_creates_data_directory(self):
        assert Path(self.temp_dir).exists()
        assert Path(self.temp_dir).is_dir()

    def test_repository_creates_json_file(self):
        file_path = Path(self.temp_dir) / "clientes.json"
        assert file_path.exists()

    def test_save_cliente_successfully(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        result = self.repository.save(cliente)
        assert result is True

    def test_save_cliente_prevents_duplicate_id(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        result = self.repository.save(cliente)
        assert result is False

    def test_find_by_id_existing_cliente(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        found = self.repository.find_by_id("client-123")

        assert found is not None
        assert found.id == "client-123"
        assert found.nome == "Empresa Teste"
        assert found.email == "test@example.com"
        assert found.cnpj == "12345678901234"

    def test_find_by_id_nonexistent_cliente(self):
        found = self.repository.find_by_id("nonexistent")
        assert found is None

    def test_find_by_email_existing_cliente(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        found = self.repository.find_by_email("test@example.com")

        assert found is not None
        assert found.email == "test@example.com"
        assert found.nome == "Empresa Teste"

    def test_find_by_email_nonexistent_cliente(self):
        found = self.repository.find_by_email("nonexistent@example.com")
        assert found is None

    def test_exists_by_email_existing_cliente(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        exists = self.repository.exists_by_email("test@example.com")
        assert exists is True

    def test_exists_by_email_nonexistent_cliente(self):
        exists = self.repository.exists_by_email("nonexistent@example.com")
        assert exists is False

    def test_save_multiple_clientes(self):
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

        assert self.repository.save(cliente1) is True
        assert self.repository.save(cliente2) is True

        found1 = self.repository.find_by_id("client-1")
        found2 = self.repository.find_by_id("client-2")

        assert found1 is not None
        assert found2 is not None
        assert found1.email == "empresa1@test.com"
        assert found2.email == "empresa2@test.com"

    def test_save_persists_data_across_instances(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)

        new_repository = JsonClienteRepository(data_dir=self.temp_dir)
        found = new_repository.find_by_id("client-123")

        assert found is not None
        assert found.email == "test@example.com"

    def test_find_by_email_is_case_sensitive(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        found = self.repository.find_by_email("TEST@EXAMPLE.COM")
        assert found is None

    def test_repository_handles_empty_file(self):
        file_path = Path(self.temp_dir) / "clientes.json"
        file_path.write_text("", encoding="utf-8")

        repository = JsonClienteRepository(data_dir=self.temp_dir)
        found = repository.find_by_id("any-id")
        assert found is None

    def test_repository_handles_corrupted_json(self):
        file_path = Path(self.temp_dir) / "clientes.json"
        file_path.write_text("{invalid json", encoding="utf-8")

        repository = JsonClienteRepository(data_dir=self.temp_dir)
        found = repository.find_by_id("any-id")
        assert found is None

    def test_save_cliente_with_special_characters_in_nome(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Teste & Cia. Ltda.",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        found = self.repository.find_by_id("client-123")

        assert found is not None
        assert found.nome == "Empresa Teste & Cia. Ltda."

    def test_save_cliente_with_unicode_characters(self):
        cliente = Cliente(
            id="client-123",
            nome="Empresa Açúcar & Café",
            email="test@example.com",
            cnpj="12345678901234"
        )

        self.repository.save(cliente)
        found = self.repository.find_by_id("client-123")

        assert found is not None
        assert found.nome == "Empresa Açúcar & Café"

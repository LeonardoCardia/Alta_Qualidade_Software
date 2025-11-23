import pytest
import tempfile
import shutil
from pathlib import Path
from adapters.repositories.json_pedido_repository import JsonPedidoRepository
from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto


class TestJsonPedidoRepository:

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repository = JsonPedidoRepository(data_dir=self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_repository_creates_data_directory(self):
        assert Path(self.temp_dir).exists()
        assert Path(self.temp_dir).is_dir()

    def test_repository_creates_json_file(self):
        file_path = Path(self.temp_dir) / "pedidos.json"
        assert file_path.exists()

    def test_save_pedido_successfully(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        result = self.repository.save(pedido)
        assert result is True

    def test_save_pedido_prevents_duplicate_id(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        self.repository.save(pedido)
        result = self.repository.save(pedido)
        assert result is False

    def test_find_by_id_existing_pedido(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100,
            cupom="MEGA10"
        )

        self.repository.save(pedido)
        found = self.repository.find_by_id("pedido-001")

        assert found is not None
        assert found.id == "pedido-001"
        assert found.cliente_id == "client-123"
        assert found.tipo_produto == TipoProduto.DIESEL
        assert found.quantidade == 100
        assert found.cupom == "MEGA10"

    def test_find_by_id_nonexistent_pedido(self):
        found = self.repository.find_by_id("nonexistent")
        assert found is None

    def test_find_by_cliente_id_existing_pedidos(self):
        pedido1 = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        pedido2 = Pedido(
            id="pedido-002",
            cliente_id="client-123",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=200
        )

        self.repository.save(pedido1)
        self.repository.save(pedido2)

        found = self.repository.find_by_cliente_id("client-123")

        assert len(found) == 2
        assert all(p.cliente_id == "client-123" for p in found)

    def test_find_by_cliente_id_no_pedidos(self):
        found = self.repository.find_by_cliente_id("nonexistent")
        assert found == []

    def test_save_pedido_without_cupom(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.ETANOL,
            quantidade=50
        )

        self.repository.save(pedido)
        found = self.repository.find_by_id("pedido-001")

        assert found is not None
        assert found.cupom is None

    def test_save_multiple_pedidos(self):
        pedido1 = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        pedido2 = Pedido(
            id="pedido-002",
            cliente_id="client-456",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=200
        )

        assert self.repository.save(pedido1) is True
        assert self.repository.save(pedido2) is True

        found1 = self.repository.find_by_id("pedido-001")
        found2 = self.repository.find_by_id("pedido-002")

        assert found1 is not None
        assert found2 is not None

    def test_save_persists_data_across_instances(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        self.repository.save(pedido)

        new_repository = JsonPedidoRepository(data_dir=self.temp_dir)
        found = new_repository.find_by_id("pedido-001")

        assert found is not None
        assert found.tipo_produto == TipoProduto.DIESEL

    def test_find_by_cliente_id_filters_correctly(self):
        pedido1 = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        pedido2 = Pedido(
            id="pedido-002",
            cliente_id="client-456",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=200
        )

        self.repository.save(pedido1)
        self.repository.save(pedido2)

        found = self.repository.find_by_cliente_id("client-123")

        assert len(found) == 1
        assert found[0].cliente_id == "client-123"

    def test_save_pedido_with_all_product_types(self):
        for tipo in TipoProduto:
            pedido = Pedido(
                id=f"pedido-{tipo.value}",
                cliente_id="client-123",
                tipo_produto=tipo,
                quantidade=10
            )

            self.repository.save(pedido)
            found = self.repository.find_by_id(f"pedido-{tipo.value}")

            assert found is not None
            assert found.tipo_produto == tipo

    def test_repository_handles_empty_file(self):
        file_path = Path(self.temp_dir) / "pedidos.json"
        file_path.write_text("", encoding="utf-8")

        repository = JsonPedidoRepository(data_dir=self.temp_dir)
        found = repository.find_by_id("any-id")
        assert found is None

    def test_repository_handles_corrupted_json(self):
        file_path = Path(self.temp_dir) / "pedidos.json"
        file_path.write_text("{invalid json", encoding="utf-8")

        repository = JsonPedidoRepository(data_dir=self.temp_dir)
        found = repository.find_by_id("any-id")
        assert found is None

    def test_save_pedido_serializes_tipo_produto_as_value(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        self.repository.save(pedido)

        file_path = Path(self.temp_dir) / "pedidos.json"
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data[0]["tipo_produto"] == "diesel"

    def test_find_by_cliente_id_returns_empty_list_not_none(self):
        found = self.repository.find_by_cliente_id("nonexistent")
        assert found == []
        assert isinstance(found, list)

    def test_save_pedido_with_large_quantidade(self):
        pedido = Pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=10000
        )

        self.repository.save(pedido)
        found = self.repository.find_by_id("pedido-001")

        assert found is not None
        assert found.quantidade == 10000

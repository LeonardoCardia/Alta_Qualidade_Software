import pytest
from domain.entities.cupom import Cupom, CupomData
from domain.entities.produto import TipoProduto


class TestCupomData:

    def test_create_cupom_data_percentual(self):
        data = CupomData(
            codigo="TEST10",
            tipo_desconto="percentual",
            valor_desconto=0.10
        )
        assert data.codigo == "TEST10"
        assert data.tipo_desconto == "percentual"
        assert data.valor_desconto == 0.10
        assert data.produto_restrito is None

    def test_create_cupom_data_fixo(self):
        data = CupomData(
            codigo="FIXA50",
            tipo_desconto="fixo",
            valor_desconto=50.0
        )
        assert data.codigo == "FIXA50"
        assert data.tipo_desconto == "fixo"
        assert data.valor_desconto == 50.0

    def test_create_cupom_data_with_produto_restrito(self):
        data = CupomData(
            codigo="LUB5",
            tipo_desconto="fixo",
            valor_desconto=5.0,
            produto_restrito=TipoProduto.LUBRIFICANTE
        )
        assert data.produto_restrito == TipoProduto.LUBRIFICANTE

    def test_cupom_data_is_immutable(self):
        data = CupomData(
            codigo="TEST10",
            tipo_desconto="percentual",
            valor_desconto=0.10
        )
        with pytest.raises(AttributeError):
            data.codigo = "NEW10"


class TestCupom:

    def test_cupom_mega10_exists(self):
        cupom = Cupom.MEGA10
        assert cupom.value.codigo == "MEGA10"
        assert cupom.value.tipo_desconto == "percentual"
        assert cupom.value.valor_desconto == 0.10
        assert cupom.value.produto_restrito is None

    def test_cupom_novo5_exists(self):
        cupom = Cupom.NOVO5
        assert cupom.value.codigo == "NOVO5"
        assert cupom.value.tipo_desconto == "percentual"
        assert cupom.value.valor_desconto == 0.05
        assert cupom.value.produto_restrito is None

    def test_cupom_lub2_exists(self):
        cupom = Cupom.LUB2
        assert cupom.value.codigo == "LUB2"
        assert cupom.value.tipo_desconto == "fixo"
        assert cupom.value.valor_desconto == 2.00
        assert cupom.value.produto_restrito == TipoProduto.LUBRIFICANTE

    def test_cupom_enum_has_three_values(self):
        assert len(Cupom) == 3

    def test_cupom_mega10_is_percentual(self):
        assert Cupom.MEGA10.value.tipo_desconto == "percentual"

    def test_cupom_novo5_is_percentual(self):
        assert Cupom.NOVO5.value.tipo_desconto == "percentual"

    def test_cupom_lub2_is_fixo(self):
        assert Cupom.LUB2.value.tipo_desconto == "fixo"

    def test_cupom_mega10_has_no_product_restriction(self):
        assert Cupom.MEGA10.value.produto_restrito is None

    def test_cupom_novo5_has_no_product_restriction(self):
        assert Cupom.NOVO5.value.produto_restrito is None

    def test_cupom_lub2_restricted_to_lubrificante(self):
        assert Cupom.LUB2.value.produto_restrito == TipoProduto.LUBRIFICANTE

    def test_cupom_mega10_discount_value(self):
        assert Cupom.MEGA10.value.valor_desconto == 0.10

    def test_cupom_novo5_discount_value(self):
        assert Cupom.NOVO5.value.valor_desconto == 0.05

    def test_cupom_lub2_discount_value(self):
        assert Cupom.LUB2.value.valor_desconto == 2.00

    def test_all_cupoms_have_valid_data(self):
        for cupom in Cupom:
            assert isinstance(cupom.value, CupomData)
            assert cupom.value.codigo is not None
            assert cupom.value.tipo_desconto in ["percentual", "fixo"]
            assert cupom.value.valor_desconto > 0

    @pytest.mark.parametrize("cupom,expected_codigo", [
        (Cupom.MEGA10, "MEGA10"),
        (Cupom.NOVO5, "NOVO5"),
        (Cupom.LUB2, "LUB2"),
    ])
    def test_cupom_codigos(self, cupom, expected_codigo):
        assert cupom.value.codigo == expected_codigo

    def test_cupom_enum_by_name(self):
        cupom = Cupom["MEGA10"]
        assert cupom == Cupom.MEGA10

    def test_iterate_over_cupoms(self):
        cupom_list = list(Cupom)
        assert len(cupom_list) == 3
        assert Cupom.MEGA10 in cupom_list
        assert Cupom.NOVO5 in cupom_list
        assert Cupom.LUB2 in cupom_list

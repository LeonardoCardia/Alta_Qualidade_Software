import pytest
from domain.value_objects.cnpj import CNPJ


class TestCNPJ:

    def test_create_valid_cnpj_plain_digits(self):
        cnpj = CNPJ("12345678901234")
        assert cnpj.value == "12345678901234"

    def test_create_valid_cnpj_with_formatting(self):
        cnpj = CNPJ("12.345.678/9012-34")
        assert cnpj.value == "12345678901234"

    def test_create_valid_cnpj_with_dots_and_slash(self):
        cnpj = CNPJ("11.222.333/0001-44")
        assert cnpj.value == "11222333000144"

    def test_create_valid_cnpj_with_mixed_formatting(self):
        cnpj = CNPJ("99.888.777/0001-55")
        assert cnpj.value == "99888777000155"

    def test_empty_cnpj_raises_error(self):
        with pytest.raises(ValueError, match="CNPJ cannot be empty"):
            CNPJ("")

    def test_cnpj_with_less_than_14_digits_raises_error(self):
        with pytest.raises(ValueError, match="Invalid CNPJ format.*Must contain 14 digits"):
            CNPJ("1234567890123")

    def test_cnpj_with_more_than_14_digits_raises_error(self):
        with pytest.raises(ValueError, match="Invalid CNPJ format.*Must contain 14 digits"):
            CNPJ("123456789012345")

    def test_cnpj_with_letters_raises_error(self):
        with pytest.raises(ValueError, match="Invalid CNPJ format.*Must contain 14 digits"):
            CNPJ("12345678901ABC")

    def test_cnpj_with_special_characters_only_raises_error(self):
        with pytest.raises(ValueError, match="Invalid CNPJ format.*Must contain 14 digits"):
            CNPJ("@@.###.$$$")

    def test_cnpj_with_spaces_raises_error(self):
        with pytest.raises(ValueError, match="Invalid CNPJ format.*Must contain 14 digits"):
            CNPJ("12 345 678 9012 34")

    def test_cnpj_formatted_output(self):
        cnpj = CNPJ("12345678901234")
        assert cnpj.formatted() == "12.345.678/9012-34"

    def test_cnpj_formatted_with_zeros(self):
        cnpj = CNPJ("00000000000000")
        assert cnpj.formatted() == "00.000.000/0000-00"

    def test_cnpj_formatted_from_formatted_input(self):
        cnpj = CNPJ("11.222.333/0001-44")
        assert cnpj.formatted() == "11.222.333/0001-44"

    def test_cnpj_str_representation(self):
        cnpj = CNPJ("12345678901234")
        assert str(cnpj) == "12345678901234"

    def test_cnpj_str_representation_after_formatting_cleanup(self):
        cnpj = CNPJ("12.345.678/9012-34")
        assert str(cnpj) == "12345678901234"

    def test_cnpj_is_immutable(self):
        cnpj = CNPJ("12345678901234")
        with pytest.raises(AttributeError):
            cnpj.value = "98765432109876"

    def test_cnpj_removes_hyphens(self):
        cnpj = CNPJ("12-345-678-9012-34")
        assert cnpj.value == "12345678901234"

    def test_cnpj_removes_all_non_digit_characters(self):
        cnpj = CNPJ("12.345.678/9012-34")
        assert cnpj.value == "12345678901234"

    @pytest.mark.parametrize("valid_cnpj,expected_clean", [
        ("12345678901234", "12345678901234"),
        ("12.345.678/9012-34", "12345678901234"),
        ("11.222.333/0001-44", "11222333000144"),
        ("00.000.000/0000-00", "00000000000000"),
        ("99-999-999-9999-99", "99999999999999"),
    ])
    def test_valid_cnpj_formats(self, valid_cnpj, expected_clean):
        cnpj = CNPJ(valid_cnpj)
        assert cnpj.value == expected_clean

    @pytest.mark.parametrize("invalid_cnpj", [
        "",
        "123",
        "1234567890123",
        "123456789012345",
        "12345678901ABC",
        "ABCDEFGHIJKLMN",
        "12.345.678/9012",
        "12.345.678",
    ])
    def test_invalid_cnpj_formats(self, invalid_cnpj):
        with pytest.raises(ValueError):
            CNPJ(invalid_cnpj)

    def test_cnpj_formatted_structure(self):
        cnpj = CNPJ("11222333000144")
        formatted = cnpj.formatted()
        assert formatted == "11.222.333/0001-44"
        assert formatted[2] == "."
        assert formatted[6] == "."
        assert formatted[10] == "/"
        assert formatted[15] == "-"

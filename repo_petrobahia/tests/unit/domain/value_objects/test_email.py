import pytest
from domain.value_objects.email import Email


class TestEmail:

    def test_create_valid_email(self):
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_email_with_subdomain(self):
        email = Email("user@mail.company.com")
        assert email.value == "user@mail.company.com"

    def test_email_with_plus_sign(self):
        email = Email("user+tag@example.com")
        assert email.value == "user+tag@example.com"

    def test_email_with_numbers(self):
        email = Email("user123@example456.com")
        assert email.value == "user123@example456.com"

    def test_email_with_dots_in_local_part(self):
        email = Email("first.last@example.com")
        assert email.value == "first.last@example.com"

    def test_email_with_underscore(self):
        email = Email("user_name@example.com")
        assert email.value == "user_name@example.com"

    def test_email_with_hyphen_in_domain(self):
        email = Email("user@my-company.com")
        assert email.value == "user@my-company.com"

    def test_empty_email_raises_error(self):
        with pytest.raises(ValueError, match="Email cannot be empty"):
            Email("")

    def test_email_without_at_sign_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("invalidemail.com")

    def test_email_without_domain_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("user@")

    def test_email_without_local_part_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("@example.com")

    def test_email_without_tld_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("user@example")

    def test_email_with_spaces_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("user name@example.com")

    def test_email_with_multiple_at_signs_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("user@@example.com")

    def test_email_with_single_character_tld(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("user@example.c")

    def test_email_str_representation(self):
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

    def test_email_is_immutable(self):
        email = Email("test@example.com")
        with pytest.raises(AttributeError):
            email.value = "new@example.com"

    @pytest.mark.parametrize("valid_email", [
        "simple@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "user_123@sub.domain.com",
        "a@b.co",
        "test.email.with.multiple.dots@example.com",
    ])
    def test_valid_email_formats(self, valid_email):
        email = Email(valid_email)
        assert email.value == valid_email

    @pytest.mark.parametrize("invalid_email", [
        "plaintext",
        "@example.com",
        "user@",
        "user name@example.com",
        "user@example",
        "user@@example.com",
        "user@.com",
        "",
    ])
    def test_invalid_email_formats(self, invalid_email):
        with pytest.raises(ValueError):
            Email(invalid_email)

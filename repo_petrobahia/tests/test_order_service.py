import pytest

from legacy import order_service

def test_import_order_service_module():
    assert order_service is not None
import pytest

from legacy import clients

def test_import_clients_module():
    assert clients is not None
from typing import Dict

import pytest as pytest


@pytest.fixture
def customer_data() -> Dict:
    return {
        "name": "Test Customer",
        "phone": "01115789524",
        "email": "test@gmail.com",
        "address": "test address"
    }


@pytest.fixture
def updated_customer_data() -> Dict:
    return {
        "name": "Test Customer updated",
        "address": "test address updated"
    }

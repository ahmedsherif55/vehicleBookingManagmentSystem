import pytest
import requests

DEFAULT_ROUTE = 'http://127.0.0.1:5000/api'


@pytest.mark.unit
def test_get_customer():
    response = requests.get(f"{DEFAULT_ROUTE}/customers/1")
    customer = response.json()['data']
    assert response.status_code == 200
    assert customer['id'] == 1


@pytest.mark.unit
def test_add_customer(customer_data):
    response = requests.post(f"{DEFAULT_ROUTE}/customers", json=customer_data)
    customer = response.json()['data']
    assert response.status_code == 200
    assert customer['email'] == customer_data['email']


@pytest.mark.unit
def test_update_customer(updated_customer_data):
    response = requests.put(f"{DEFAULT_ROUTE}/customers/1", json=updated_customer_data)
    customer = response.json()['data']
    assert response.status_code == 200
    assert customer['name'] == updated_customer_data['name']


@pytest.mark.unit
def test_delete_customer():
    response = requests.delete(f"{DEFAULT_ROUTE}/customers/1")
    assert response.status_code == 200

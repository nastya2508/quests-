import pytest
from order_manager import Order

@pytest.fixture
def sample_order():
    items = [
        {"price": 10.0, "quantity": 2},
        {"price": 21.75, "quantity": 1}
    ]
    return Order("A-1", items)

def test_order_total(sample_order):
    assert sample_order.total() == pytest.approx(41.75)

def test_order_total_empty():
    order = Order("A-2", [])
    assert order.total() == 0.0

def test_most_expensive_returns_highest_price(sample_order):
    assert sample_order.most_expensive() is sample_order.items[1]

def test_most_expensive_uses_unit_price_not_quantity():
    items = [
        {"price": 5.0, "quantity": 100},
        {"price": 20.0, "quantity": 1},
        {"price": 10.0, "quantity": 2},
    ]
    assert Order("A-1", items).most_expensive() is items[1]

def test_most_expensive_with_one_item():
    item = {"price": 4.0, "quantity": 1}
    assert Order("A-1", [item]).most_expensive() is item

def test_most_expensive_with_equal_prices_returns_first():
    items = [
        {"price": 10.0, "quantity": 1},
        {"price": 10.0, "quantity": 3},
    ]
    assert Order("A-1", items).most_expensive() is items[0]

def test_most_expensive_with_empty_items_raises_value_error():
    with pytest.raises(ValueError):
        Order("A-1", []).most_expensive()

@pytest.mark.parametrize("percent, expected_prices", [
    (0, [10.0, 3.0, 7.5]),
    (10, [9.0, 2.7, 6.75]),
    (50, [5.0, 1.5, 3.75]),
    (100, [0.0, 0.0, 0.0]),
])
def test_apply_discount_changes_prices(percent, expected_prices):
    items = [
        {"price": 10.0, "quantity": 1},
        {"price": 3.0, "quantity": 1},
        {"price": 7.5, "quantity": 1},
    ]
    order = Order("A-1", items)
    order.apply_discount(percent)
    actual_prices = [item["price"] for item in order.items]
    assert actual_prices == pytest.approx(expected_prices)

@pytest.mark.parametrize("invalid_percent", [-1, 101, "invalid"])
def test_apply_discount_invalid_raises_value_error(invalid_percent):
    order = Order("A-1", [{"price": 10.0, "quantity": 1}])
    with pytest.raises(ValueError):
        order.apply_discount(invalid_percent)

def test_order_repr():
    order = Order("A-1", [{"price": 10.0, "quantity": 1}])
    assert repr(order) == "Order(order_id='A-1', items=[{'price': 10.0, 'quantity': 1}])"
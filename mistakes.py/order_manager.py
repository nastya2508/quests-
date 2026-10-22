class Order:
    def __init__(self, order_id: str, items: list[dict]):
        self.order_id = order_id
        self.items = items

    def total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    def most_expensive(self) -> dict:
        if not self.items:
            raise ValueError("Items list is empty")
        return max(self.items, key=lambda x: x["price"])

    def apply_discount(self, percent: float) -> None:
        if not isinstance(percent, (int, float)) or not (0 <= percent <= 100):
            raise ValueError("Invalid discount percentage")
        multiplier = 1 - percent / 100
        for item in self.items:
            item["price"] = round(item["price"] * multiplier, 2)

    def __repr__(self) -> str:
        return f"Order(order_id='{self.order_id}', items={self.items})"
from dataclasses import dataclass


@dataclass
class PaymentsCustomer:
    id: int
    amount: float
    customer_id: int
    product_name: str
    quantity: int
    created_at: str
    updated_at: str

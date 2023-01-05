from api.engine.domain.entities import entities_customers
from api.engine.domain.entities import entities_payments


def constructor_customer_entities(customer_orm) -> entities_customers.Customer:
    return entities_customers.Customer(
        id=customer_orm.id,
        name=customer_orm.name,
        paternal_surname=customer_orm.paternal_surname,
        email=customer_orm.email,
    )


def constructor_payment_entities(payment_orm) -> entities_payments.PaymentsCustomer:
    return entities_payments.PaymentsCustomer(
        id=payment_orm.id,
        customer_id=payment_orm.customer_id,
        amount=payment_orm.amount,
        product_name=payment_orm.product_name,
        quantity=payment_orm.quantity,
        created_at=payment_orm.created_at,
        updated_at=payment_orm.updated_at,
    )


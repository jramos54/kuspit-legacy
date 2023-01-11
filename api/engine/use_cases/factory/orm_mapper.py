# Librerias Estandar
import typing

from api.engine.domain.entities import (
    entities_frequent_questions,
    entities_user_secure_code,
    entities_customers,
    entities_products,
    entities_payments,
    entities_accounts,
    entities_users,
    entities_banks,
    entities_beneficiaries,
    entities_movement,
    entities_movement_historical,
    entities_recipient_accounts,
    entities_recipient,
    entities_user_dashboard,
    entities_operadores
)


def constructor_frequent_questions_entities(
    frequent_questions_orm,
) -> entities_frequent_questions.FrequentQuestions:
    """contructor for frequent questions entities"""
    return entities_frequent_questions.FrequentQuestions(
        id=frequent_questions_orm.id,
        question=frequent_questions_orm.question,
        answer=frequent_questions_orm.answer,
        is_active=frequent_questions_orm.is_active,
    )


def constructor_products(
    products_orm,
) -> entities_products.Products:
    """contructor for product entities"""
    return entities_products.Products(
        idproducto=products_orm.idproducto,
        nombre=products_orm.nombre,
    )


def constructor_movement(movement_orm) -> entities_movement.Movement:
    return entities_movement.Movement(
        fecha_elaboracion=movement_orm.fecha_elaboracion,
        fecha_pago=movement_orm.fecha_pago,
        movimiento=movement_orm.movimiento,
        estatus=movement_orm.estatus,
        destinatario=movement_orm.destinatario,
        cuenta_bancaria=movement_orm.cuenta_bancaria,
        monto=movement_orm.monto,
        concepto=movement_orm.concepto,
        clave_rastreo=movement_orm.clave_rastreo,
        referencia=movement_orm.referencia,
        info=movement_orm.info,
    )


def constructor_account(account_orm) -> entities_accounts.Accounts:
    return entities_accounts.Accounts(
        # name=account_orm.name,
        alias=account_orm.alias,
        type_account=account_orm.type_account,
    )


def constructor_recipient(recipient_orm) -> entities_recipient.Recipient:
    return entities_recipient.Recipient(
        iddestinatario=recipient_orm.iddestinatario,
        nombre=recipient_orm.nombre,
        paterno=recipient_orm.paterno,
        materno=recipient_orm.materno,
        rfc=recipient_orm.rfc,
        curp=recipient_orm.curp,
        is_active=recipient_orm.is_active,
        correo=recipient_orm.correo,
        pfisica=recipient_orm.pfisica,
        cuentas=recipient_orm.cuentas
    )


def constructor_persona_fisica(user_orm) -> entities_users.UserDyP:
    return entities_users.UserDyP(
        **user_orm,
    )


def constructor_persona_moral(user_orm) -> entities_users.UserDyP:
    return entities_users.UserDyP(
        **user_orm,
    )


def constructor_customer_entities(customer_orm) -> entities_customers.Customer:
    return entities_customers.Customer(
        id=customer_orm.id,
        name=customer_orm.name,
        paternal_surname=customer_orm.paternal_surname,
        email=customer_orm.email,
    )


def constructor_payment_entities(payment_orm) -> entities_payments.Payments:
    return entities_payments.Payments(
        kauxiliar=payment_orm.kauxiliar,
        id_recipient=payment_orm.id_recipient,
        id_account=payment_orm.id_account,
        amount=payment_orm.amount,
        description=payment_orm.description,
        payment_date=payment_orm.payment_date,
        reference=payment_orm.reference,
        payment_hour=payment_orm.payment_hour,
    )


def constructor_payment_openfin_entities(
    payment_orm,
) -> entities_payments.PaymentsOpenFin:
    monto = float(payment_orm["Monto"].replace(",", ""))
    comision = 5.0
    IVA = comision * 0.16
    total = monto + comision + IVA
    return entities_payments.PaymentsOpenFin(
        amount=payment_orm["Monto"],
        status=payment_orm["Estatus"],
        row_id=payment_orm["__rowId"],
        row_info=payment_orm["__rowInfo"],
        payment_date=payment_orm["Fecha Pago"],
        pactivo=payment_orm["___pactivo"],
        wactiva=payment_orm["___wactiva"],
        scheduled_time=payment_orm["H. Programada"],
        alias=payment_orm["Nombre wallet"],
        programed=payment_orm["___programado"],
        creation_date=payment_orm["fecha elaboracion"],
        intension_date=payment_orm["Fecha intención"],
        reference=payment_orm["referencia"],
        description=payment_orm["descripcion"],
        bank_institution=None,
        num_account=None,
        comision=comision,
        IVA=IVA,
        total=total,
        RFC=None,
        CURP=None,
    )


def constructor_user_entities(user_orm) -> entities_users.UserDyP:
    return entities_users.UserDyP(
        id=user_orm.id,
        username=user_orm.username,
        email=user_orm.email,
        is_active=user_orm.is_active,
        is_staff=user_orm.is_staff,
        is_superuser=user_orm.is_superuser,
        is_customer=user_orm.is_customer,
        is_persona_fisica=user_orm.is_persona_fisica,
        is_persona_moral=user_orm.is_persona_moral,
    )


def constructor_user_secure_code_entities(
    secure_code_orm,
) -> typing.Optional[entities_user_secure_code.UserSecureCode]:
    if secure_code_orm is None:
        return None
    return entities_user_secure_code.UserSecureCode(
        id=secure_code_orm.id,
        user_id=secure_code_orm.user_id,
        code=secure_code_orm.code,
        expedition_datetime=secure_code_orm.expedition_datetime,
        tries=secure_code_orm.tries,
        is_active=secure_code_orm.is_active,
    )


def constructor_beneficiary(user_orm) -> entities_users.UserDyP:
    return entities_users.UserDyP(
        **user_orm,
    )


def constructor_movement_by_month(historical_orm) -> entities_movement_historical.MovementByMonth:
    return entities_movement_historical.MovementByMonth(
        mes=historical_orm.mes,
        depositos=historical_orm.depositos,
        retiros=historical_orm.retiros,
        pago_servicios=historical_orm.pago_servicios,
        retiros_programados=historical_orm.retiros_programados,
        current=historical_orm.current
    )


def constructor_user_dashboard(dashboard_orm) -> entities_user_dashboard.UserDashboard:
    return entities_user_dashboard.UserDashboard(
        nombre=dashboard_orm.nombre,
        correo=dashboard_orm.correo
    )


def constructor_bank(bank_orm) -> entities_banks.Bank:
    return entities_banks.Bank(
        key=bank_orm.key,
        nombre=bank_orm.nombre,
        nombre_completo=bank_orm.nombre_completo,
        rfc=bank_orm.rfc,
    )


def constructor_recipient_account(recipient_account_orm) -> entities_recipient_accounts.RecipientAccount:
    return entities_recipient_accounts.RecipientAccount(
        idcuenta=recipient_account_orm.idcuenta,
        cuenta=recipient_account_orm.cuenta,
        institucion_bancaria=recipient_account_orm.institucion_bancaria,
        catalogo_cuenta=recipient_account_orm.catalogo_cuenta,
        is_active=recipient_account_orm.is_active,
        limite_operaciones=recipient_account_orm.limite_operaciones,
        limite=recipient_account_orm.limite,
        alias=recipient_account_orm.alias,
    )


def constructor_operator(operator_orm) -> entities_operadores.Operator:
    return entities_operadores.Operator(
        idoperador=operator_orm.idoperador,
        kasociado=operator_orm.kasociado,
        nombre=operator_orm.nombre,
        email=operator_orm.email,
        ingreso=operator_orm.ingreso,
        acceso=operator_orm.acceso,
        permisos=operator_orm.permisos
        )



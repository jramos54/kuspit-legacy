@severity=normal
Feature: Servicio de Wallets

    Background:
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password    |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario 

    Scenario: Listar los productos que existen
        Given El url "$PRODUCTS"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "El listado de productos fue exitoso"
        Then Se valida el esquema para productos

    Scenario Outline: Listar los productos por id
        Given El url "$PRODUCTS"
        And Los params enviados en la solicitud
        | key       | Value        |
        | idproducto| <idproducto> |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "El producto se obtuvo exitosamente"
        Then Se valida el esquema para productos
        Examples:
            |idproducto|
            |2001|
            |2003|
            |2004|
            |2002|

    Scenario: Listar los productos que no existen
        Given El url "$PRODUCTS"
        And Los params enviados en la solicitud
        | key       | Value |
        | idproducto| 1999  |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "Producto no encontrado"

    Scenario: Listar las wallets que tiene el usuario
        Given El url "$WALLETS"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Wallets disponibles"
        Then Se valida el esquema para wallets
    
    Scenario: Listar la wallet por kauxiliar
        Given El url "$WALLETS"
        And Los params enviados en la solicitud
        | key       | Value |
        | kauxiliar | 44    |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Detalle de wallet"
        Then Se valida el esquema para wallets
    
    Scenario: Listar una wallet por kauxiliar que no existe
        Given El url "$WALLETS"
        And Los params enviados en la solicitud
        | key       | Value |
        | kauxiliar | 14    |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "Cuenta no encontrado"

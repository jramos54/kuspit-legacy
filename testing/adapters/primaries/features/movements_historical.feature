@severity=normal
Feature: Servicio de Historico de Movimientos


    Background:
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario 

    Scenario: Buscar Movimientos cuando la cuenta no existe
        Given El url "$MOVEMENTS_HISTORICAL"
        And Los params enviados en la solicitud
        | key       | Value     |
        | kauxiliar | 0         |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "404"
        Then Se recibe un mensaje "Cuenta no existente"


    Scenario: Listar el historico de movimientos
        Given El url "$MOVEMENTS_HISTORICAL"
        And Los params enviados en la solicitud
        | key       | Value |
        | kauxiliar | 44    |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el numero de elementos en la respuesta menor a 12
        Then Se valida el esquema de la respuesta de Movimientos Historico

    Scenario: Validar el mes actual como activo
        Given El url "$MOVEMENTS_HISTORICAL"
        And Los params enviados en la solicitud
        | key       | Value |
        | kauxiliar | 44    |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el numero de elementos en la respuesta menor a 12
        Then Se valida el esquema de la respuesta de Movimientos Historico
        Then se valida el mes actual
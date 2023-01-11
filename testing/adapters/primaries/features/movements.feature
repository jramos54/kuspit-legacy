@severity=normal
Feature: Servicio de Movimientos


    Background:
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario 

    Scenario: Buscar Movimientos cuando la cuenta no existe
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value     |
        | kauxiliar | 0         |
        | defecha   | 2024-1-1  |
        | afecha    | 2024-12-28|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "404"
        Then Se recibe un mensaje "Cuenta no existente"


    Scenario Outline: Listar todos los movimientos por Fecha
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value       |
        | kauxiliar | <kauxiliar> |
        | defecha   | <defecha>   |
        | afecha    | <afecha>    |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se valida el esquema de la respuesta de Movimientos

        Examples: 
            | kauxiliar | defecha | afecha |
            # Por el periodo de dos años
            |   44      | 2024-1-1         |  2024-12-31      |  
            # Por cada Bimestre
            |   44      | 2024-1-1         |  2024-2-28      |  
            |   44      | 2024-3-1         |  2024-4-30      |  
            |   44      | 2024-5-1         |  2024-6-30      |  
            |   44      | 2024-7-1         |  2024-8-31      |  
            |   44      | 2024-9-1         |  2024-10-31      |  
            |   44      | 2024-11-1         |  2024-12-31      |  
            # Por Mes
            |   44      | 2024-1-1         |  2024-1-31      |  
            |   44      | 2024-2-1         |  2024-2-28      |  
            |   44      | 2024-3-1         |  2024-3-31      |  
            |   44      | 2024-4-1         |  2024-4-30      |  
            |   44      | 2024-5-1         |  2024-5-31      |  
            |   44      | 2024-6-1         |  2024-6-30      |  
            |   44      | 2024-7-1         |  2024-7-31      |  
            |   44      | 2024-8-1         |  2024-8-31      |  
            |   44      | 2024-9-1         |  2024-9-30      |  
            |   44      | 2024-10-1         |  2024-10-31      |  
            |   44      | 2024-11-1         |  2024-11-30      |  
            |   44      | 2024-12-1         |  2024-12-31      |  

    Scenario: Se introduce una fecha final menor a la fecha inicial
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value     |
        | kauxiliar | 44         |
        | defecha   | 2024-1-1  |
        | afecha    | 2023-12-28|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "400"
        Then Se recibe un mensaje "defecha no puede ser mayor que afecha"
    
    Scenario: No hay movimientos en el periodo 
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value     |
        | kauxiliar | 44         |
        | defecha   | 2023-1-1  |
        | afecha    | 2023-1-31|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "No hay Movimientos en el periodo"
        Then Se valida que no hay movimientos en la respuesta

    Scenario Outline: Listar todos los movimientos limitando el numero de movimientos
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value      |
        | kauxiliar | 44         |
        | defecha   | 2024-1-1   |
        | afecha    | 2024-12-31 |
        | limite    | <limite>   |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el esquema de la respuesta de Movimientos
        Then El numero de movimientos es menor al "<limite>"

        Examples:
        |limite|
        | 0    |
        |1     |
        |100   |
        |37    |

    Scenario Outline: Filtrar los movimientos por tipo de movimiento
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value      |
        | kauxiliar | 44         |
        | defecha   | 2024-1-1   |
        | afecha    | 2024-12-31 |
        | movimiento| <movimiento>|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el esquema de la respuesta de Movimientos
        Then Se validan el tipo de movimiento es "<movimiento>"

        Examples:
        |movimiento|
        | Retiro   |
        | Depósito |
        | Servicio |
        | Impuesto |
    
    Scenario Outline: Filtrar los movimientos por tipo de estatus
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value      |
        | kauxiliar | 44         |
        | defecha   | 2024-1-1   |
        | afecha    | 2024-12-31 |
        | estatus   | <estatus>  |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el esquema de la respuesta de Movimientos
        Then Se validan el estatus "<estatus_recibido>" del movimiento

        Examples:
        | estatus   | estatus_recibido |
        | Pendiente | Pendiente        |
        | Enviada   | Enviada          |
        | Liquidado | Liquidado        |
        | Enviado   | Enviada          |
        | Liquidada | Liquidado        |
        | Cancelada | Cancelada        |
        | Cancelado | Cancelada        |

    Scenario Outline: Filtrar los movimientos por tipo de movimiento y estatus
        Given El url "$MOVEMENTS"
        And Los params enviados en la solicitud
        | key       | Value      |
        | kauxiliar | 44         |
        | defecha   | 2024-1-1   |
        | afecha    | 2024-12-31 |
        | estatus   | <estatus>  |
        | movimiento| <movimiento>|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de movimientos exitosa"
        Then Se valida el esquema de la respuesta de Movimientos
        Then Valida el tipo de movimiento es "<movimiento>" y el estatus "<estatus_recibido>"

        Examples:
        | estatus   |movimiento  | estatus_recibido |
        | Pendiente | Retiro     | Pendiente |
        | Enviada   | Retiro     | Enviada|
        | Liquidado | Retiro     | Liquidado|
        | Enviado   | Retiro     | Enviada|
        | Liquidada | Retiro     | Liquidado|
        | Cancelada | Retiro     | Cancelada|
        | Cancelado | Retiro     | Cancelada|
        | Pendiente | Depósito   | Pendiente|
        | Enviada   | Depósito   | Enviada|
        | Liquidado | Depósito   | Liquidado|
        | Enviado   | Depósito   | Enviada| 
        | Liquidada | Depósito   | Liquidado|
        | Cancelada | Depósito   | Cancelada|
        | Cancelado | Depósito   | Cancelada|
        | Pendiente | Servicio   | Pendiente|
        | Enviada   | Servicio   | Enviada|
        | Liquidado | Servicio   | Liquidado | 
        | Enviado   | Servicio   | Enviada|
        | Liquidada | Servicio   | Liquidado|
        | Cancelada | Servicio   | Cancelada|
        | Cancelado | Servicio   | Cancelada|
        | Pendiente | Impuesto   | Pendiente|
        | Enviada   | Impuesto   | Enviada|
        | Liquidado | Impuesto   | Liquidado|
        | Enviado   | Impuesto   | Enviada|
        | Liquidada | Impuesto   | Liquidado|
        | Cancelada | Impuesto   | Cancelada|
        | Cancelado | Impuesto   | Cancelada|
  
@severity=normal
Feature: Servicio de Operadores
        
    Scenario Outline: Listar todos los operadores en la cuenta con operadores Admin
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | <email>           | <password>    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token  
        Given El url "$OPERATORS"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de operadores exitosa"
        Then Se valida el esquema de la respuesta de Operadores
        Examples:
            | email             | password       |
            | $USER_4           | $PASSWORD_4    |
            | $OPER_3           | $PASS_OPER_3   |
        
        
    Scenario Outline: Listar a un operador por id en la cuenta con operadores Admin
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | <email>           | <password>    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token  
        Given El url "$OPERATORS"
        And Los params enviados en la solicitud
        | key        | Value |
        | idoperador | <id>  |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de operador exitosa"
        Then Se valida el esquema de la respuesta de Operadores
            
        Examples: Combinaciones
            | email     | password    | id |
            | $USER_4   | $PASSWORD_4 | 43 |
            | $USER_4   | $PASSWORD_4 | 44 |
            | $USER_4   | $PASSWORD_4 | 45 |
            | $USER_4   | $PASSWORD_4 | 46 |
            | $OPER_3   | $PASS_OPER_3| 43 |
            | $OPER_3   | $PASS_OPER_3| 44 |
            | $OPER_3   | $PASS_OPER_3| 45 |
            | $OPER_3   | $PASS_OPER_3| 46 |


    # Scenario Outline: Dar acceso a un operador por id en la cuenta con operadores Admin
    #     Given El url "$LOGIN"
    #     And Se obtienen los valores de la tabla
    #     | email             | password      |
    #     | <email>           | <password>    |
    #     When Se envia una solicitud POST
    #     Then Se valida la respuesta codigo "200"
    #     And los tokens de la sesion de usuario
    #     Then Se recibe un access token y un refresh token  
    #     Given El url "$OPERATORS"
    #     And Los params enviados en la solicitud
    #     | key        | Value |
    #     | idoperador | <id>  |
    #     When Se envia una solicitud PATCH
    #     Then Se valida la respuesta codigo "200"
    #     Then Se recibe un mensaje "Se dio acceso al operador"
    #     Given El url "$OPERATORS"
    #     And Los params enviados en la solicitud
    #     | key        | Value |
    #     | idoperador | <id>  |
    #     When Se envia una solicitud GET
    #     Then Se valida la respuesta codigo "200"
    #     Then Se recibe un mensaje "Consulta de operador exitosa"
    #     Then Se valida el esquema de la respuesta de Operadores
    #     Then El campo acceso es "<acceso>"
    #     Then El perfil del operador es "<perfil>"
        
    #     Examples: 
    #         | email     | password    | id | acceso | perfil     |
    #         | $USER_4   | $PASSWORD_4 | 43 | false  | Sin_Acceso |
    #         | $USER_4   | $PASSWORD_4 | 44 | false  | Sin_Acceso |
    #         | $USER_4   | $PASSWORD_4 | 46 | false  | Sin_Acceso |
    #         | $OPER_3   | $PASS_OPER_3| 43 | true   | Sin_Perfil |
    #         | $OPER_3   | $PASS_OPER_3| 44 | true   | Sin_Perfil |
    #         | $OPER_3   | $PASS_OPER_3| 46 | true   | Sin_Perfil |


    Scenario Outline: Asignar un perfil a un operador por id en la cuenta con operadores Admin
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | <email>           | <password>    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token  
        Given El url "$OPERATOR_ROLE"
        And Se obtienen los valores de la tabla
        | idoperador | perfil   | tipo_acceso   |
        | <id>       | <perfil> | <tipo_acceso> | 
        When Se envia una solicitud PUT
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "<mensaje_esperado>"
        Then Se valida el esquema de la respuesta de Operadores
        Given El url "$OPERATORS"
        And Los params enviados en la solicitud
        | key        | Value |
        | idoperador | <id>  |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de operador exitosa"
        Then Se valida el esquema de la respuesta de Operadores
        Then El perfil del operador es "<perfil_nuevo>"
        
        Examples: 
            | email     | password    | id |perfil            |tipo_acceso| perfil_nuevo     | mensaje_esperado |
            | $USER_4   | $PASSWORD_4 | 43 |dypfe_user        | asignar   |dypfe_user        | Se asigno el rol exitosamente|
            | $USER_4   | $PASSWORD_4 | 44 |dypfe_analista    | asignar   |dypfe_analista    | Se asigno el rol exitosamente|
            | $USER_4   | $PASSWORD_4 | 46 |dypfe_autorizador | asignar   |dypfe_autorizador | Se asigno el rol exitosamente|
            | $OPER_3   | $PASS_OPER_3| 43 |dypfe_user        | quitar    |Sin_Perfil        | Se quito el rol exitosamente|
            | $OPER_3   | $PASS_OPER_3| 44 |dypfe_analista    | quitar    |Sin_Perfil        | Se quito el rol exitosamente|
            | $OPER_3   | $PASS_OPER_3| 46 |dypfe_autorizador | quitar    |Sin_Perfil        | Se quito el rol exitosamente|
            | $USER_4   | $PASSWORD_4 | 43 |dypfe_user        | asignar   |dypfe_user        | Se asigno el rol exitosamente|
            | $USER_4   | $PASSWORD_4 | 44 |dypfe_analista    | asignar   |dypfe_analista    | Se asigno el rol exitosamente|
            | $USER_4   | $PASSWORD_4 | 46 |dypfe_autorizador | asignar   |dypfe_autorizador | Se asigno el rol exitosamente|
    

    Scenario Outline: Bloquear el servicio a operadores con rol diferente a Admin
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | <email>           | <password>    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token  
        Given El url "$OPERATORS"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "You do not have permission to perform this action."
        Given El url "$OPERATORS"
        And Se obtienen los valores de la tabla
        | nombre      | paterno     | materno |correo                | pfisica |
        | OperPrueba7 | OperPrueba7 | Prueba7 | OperPrueba7@gmail.com| true    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "You do not have permission to perform this action."
        Given El url "$OPERATORS"
        And Los params enviados en la solicitud
        | key        | Value |
        | idoperador | 44    |
        When Se envia una solicitud PATCH
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "You do not have permission to perform this action."
        Given El url "$OPERATOR_ROLE"
        And Se obtienen los valores de la tabla
        | idoperador | perfil         | tipo_acceso |
        | 44         | dypfe_analista | asignar     | 
        When Se envia una solicitud PUT
        Then Se valida la respuesta codigo "403"
        Then Se recibe un mensaje "You do not have permission to perform this action."
        Examples:
            | email             | password       |
            | $OPER_1           | $PASS_OPER_1   |
            | $OPER_2           | $PASS_OPER_2   |
            | $OPER_4           | $PASS_OPER_4   |



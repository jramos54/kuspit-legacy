@severity=normal
Feature: Servicio de Dashboard

    Scenario Outline: Obtener los datos del usuario de la cuenta
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password    |
        | <email>           | <password>  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario 
        Given El url "$DASHBOARD"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se recibe un mensaje "Consulta de usuario exitosa"
        Then Se valida el nombre "<full_name>" y asociado "<kasociado>" 

        Examples: 
            | email   | password    | full_name              | kasociado |
            | $USER_2 | $PASSWORD_2 | sistema Adminitracion del sistema  |  1       |  
            | $USER_4 | $PASSWORD_4 | Hugo Guerra Partida    |  32       |  
            | $USER_5 | $PASSWORD_5 | Almacenes Guevara S.A. de C.V.| 6  |  
            | $USER_6 | $PASSWORD_6 | Hugo Guerra Partida    |  33       |  
            | $OPER_4 | $PASS_OPER_4| Hugo Guerra Partida    |  32       |  
            | $OPER_3 | $PASS_OPER_3| Hugo Guerra Partida    |  32       |  
            | $OPER_2 | $PASS_OPER_2| Hugo Guerra Partida    |  32       |  
            | $OPER_1 | $PASS_OPER_1| Hugo Guerra Partida    |  32       |  

    @skip
    Scenario Outline: Obtener nombre de usuario por correo
        Given El url "$DASH_LOGIN"
        And Los params enviados en la solicitud
        | key   | Value   |
        | email | <email> |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then El nombre completo es "<full_name>" y es nuevo usuario "<is_new_user>"

        Examples: 
            | email                      | full_name              | is_new_user |
            | demo@sinc.com.mx           | openfin_user           |  False      |  
            | joel.ramos@kuspit.com      | Hugo Guerra Partida    |  False      |  
            | raudys.rodriguez@kuspit.com| Almacenes Guevara      |  False      |  
            | jacob.munoz@kuspit.com     | Jacob Munoz            |  True       |  
            | carlos.jarero@kuspit.com   | Hugo Guerra Partid     |  False      |  
            | paul.ibarra@kuspit.com     | Paul Ibarra            |  True       |  
            | tony.stark@gmail.com       | Tony Stark             |  True       |  
            | jhon.wick@gmail.com        | John Wick Estrada      |  True       |  
            | Operador2@gmail.com        | Operador2 Kuspit Prueba|  True       |  
            | Operador1@gmail.com        | Operador1 Kuspit Prueba|  True       |  

    @skip
    Scenario Outline: Cambiar el estatus de nuevo usuario
        Given El url "$DASH_NEW"
        And Los params enviados en la solicitud
        | key   | Value   |
        | email | <email> |
        When Se envia una solicitud PATCH
        Then Se valida la respuesta codigo "200"
        Then El nombre completo es "<full_name>" y es nuevo usuario "<is_new_user>"

        Examples: 
            | email                      | full_name              | is_new_user |
            | tony.stark@gmail.com       | Tony Stark             |  False      |  
            | jhon.wick@gmail.com        | John Wick Estrada      |  False      |  
            | Operador2@gmail.com        | Operador2 Kuspit Prueba|  False      |  
            | Operador1@gmail.com        | Operador1 Kuspit Prueba|  False      |  
            | tony.stark@gmail.com       | Tony Stark             |  True       |  
            | jhon.wick@gmail.com        | John Wick Estrada      |  True       |  
            | Operador2@gmail.com        | Operador2 Kuspit Prueba|  True       |  
            | Operador1@gmail.com        | Operador1 Kuspit Prueba|  True       |  
            

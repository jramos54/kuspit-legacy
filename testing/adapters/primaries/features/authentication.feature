@severity=blocker
Feature: Servicio de Login


    Scenario: Hacer login con un usuario activo
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token  

    @skip
    Scenario: Hacer login con un correo no registrado
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email                           | password      |
        | user@noregistrado.com           |$PASSWORD_3    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje "Este correo no está registrado, ¿Deseas registrarte?"

    Scenario: Hacer login con una contraseña incorrecta
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_5  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje "La contraseña o token son incorrectos, después de 3 intentos tu cuenta será bloqueada."
        Then Se hace una espera de "3" segundos
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token

    Scenario: Hacer login tres intentos con una contraseña incorrecta
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_5  |
        When Se realizan los siguientes intentos
        |intento|codigo |mensaje                                                                               |espera|
        |1      |401    |La contraseña o token son incorrectos, después de 3 intentos tu cuenta será bloqueada.|5     |
        |2      |401    |La contraseña o token son incorrectos, después de 3 intentos tu cuenta será bloqueada.|5     |
        |3      |401    |La contraseña o token son incorrectos, después de 3 intentos tu cuenta será bloqueada.|5     |
        # Se hace el login correcto pero tiene que esperar 10 minutos
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje "Por seguridad tu cuenta ha sido bloqueada, intenta de nuevo en 10 minutos a partir de este momento."
        Then Se hace una espera de "600" segundos
        # despues de los 10 minutos, el proceso continua como debe
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token

    @skip 
    Scenario: Hacer login con una cuenta inactiva
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password    |
        | $USER_1           |$PASSWORD_1  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje
        """
        Tu cuenta se encuentra Inactiva.
        Para poder acceder nuevamente comunicate con el Centro de Atención a Usuarios DyP:
        800 110 90 90
        En horario de atención:
        Lunes a viernes de 08:00 a 20:00 horas, sábados de 08:00 a 15:00 horas.
        O escribenos a: clientes@depositosypagos.com
        """
   
    @skip
    Scenario: Hacer login con una cuenta bloqueada
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password    |
        | $USER_3           |$PASSWORD_3  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje
        """
        Por seguridad tu cuenta ha sido bloqueada. Para poder acceder nuevamente comunicate con el Centro de Atención a Usuarios DyP:
        800 110 90 90
        En horario de atención: Lunes a viernes de 08:00 a 20:00 horas, sábados de 08:00 a 15:00 horas.
        O escribenos a: clientes@depositosypagos.com
        """
    
    Scenario: Hacer login con una cuenta que tiene una sesion activa
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "401"
        Then Se recibe un mensaje "Actualmente ya cuentas con una sesión abierta,para poder iniciar una nueva asegurate de cerrar la anterior."
        Then Se hace una espera de "600" segundos
        # despues de los 5 minutos, el proceso continua como debe
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token

    Scenario Outline: Hacer login con varios usuarios 
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | <email>           | <password>    |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario
        Then Se recibe un access token y un refresh token 
        Examples:
            | email             | password      |
            | $USER_4           | $PASSWORD_4   |
            | $OPER_1           | $PASS_OPER_1   |
            | $OPER_2           | $PASS_OPER_2   |
            | $OPER_3           | $PASS_OPER_3   |
            | $OPER_4           | $PASS_OPER_4   |

    # Scenario: Comparar el tiempo de expiracion de DyP con el de OpenFin
    #     Given El url "$LOGIN"
    #     And Se obtienen los valores de la tabla
    #     | email             | password      |
    #     | $USER_4           |$PASSWORD_4  |
    #     When Se envia una solicitud POST
    #     Then Se valida la respuesta codigo "200"
    #     Then Se recibe un access token y un refresh token
    #     Then Se valida el tiempo de expiracion entre tokens
    
    # Scenario: Validar los tiempos de expiracion del access token y refresh token
    #     Given El url "$LOGIN"
    #     And Se obtienen los valores de la tabla
    #     | email             | password      |
    #     | $USER_4           |$PASSWORD_4  |
    #     When Se envia una solicitud POST
    #     Then Se valida la respuesta codigo "200"
    #     And los tokens de la sesion de usuario
    #     Then Se recibe un access token y un refresh token
    #     Then Se hace una espera de "300" segundos
    #     Given El url "$RECIPIENT"
    #     And los tokens de la sesion de usuario
    #     When Se envia una solicitud GET
    #     Then Se valida la respuesta codigo "401"
    #     Then Se recibe un mensaje "Given token not valid for any token type" 
    #     Then Se hace una espera de "180" segundos 
    #     Given El url "$REFRESH"
    #     And los tokens de la sesion de usuario
    #     When Se envia una solicitud POST
    #     Then Se valida la respuesta codigo "200"
    #     Then Se recibe un access token y un refresh token
    #     Given El url "$RECIPIENT"
    #     And los tokens de la sesion de usuario
    #     When Se envia una solicitud GET
    #     Then Se valida la respuesta codigo "200"




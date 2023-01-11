@severity=blocker
Feature: Servicio de destinatarios

# se realiza el login
    Background:
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password    |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario    

    Scenario: Listar los destinatarios que el usuario tiene registrados en DyP
        Given El url "$RECIPIENT"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        # And Se valida la respuesta con el schema de destinatario
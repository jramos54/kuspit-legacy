@severity=normal
Feature: Servicio de Bancos


    Background:
        Given El url "$LOGIN"
        And Se obtienen los valores de la tabla
        | email             | password      |
        | $USER_4           |$PASSWORD_4  |
        When Se envia una solicitud POST
        Then Se valida la respuesta codigo "200"
        And los tokens de la sesion de usuario 

    Scenario: Listar todos los bancos registrados
        Given El url "$BANK"
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se valida el esquema de la respuesta de Bancos

    @dynamic_banks
    Scenario Outline: Buscar Banco por Nombre
        Given El url "$BANK"
        And Los params enviados en la solicitud
        | key    | Value   |
        | nombre | <nombre> |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se valida el esquema de la respuesta de Bancos
        Then Se valida la informacion del banco "<nombre>", clave "<key>", rfc "<rfc>" y nombre completo "<nombre_completo>"

        Examples: Dynamic
            | nombre | key | rfc | nombre_completo |
            |   .    |  .  |  .  |       .         |

    
    Scenario Outline: Buscar Banco por CLABE
        Given El url "$BANK"
        And Los params enviados en la solicitud
        | key    | Value   |
        | clabe  | <clabe> |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "200"
        Then Se valida el esquema de la respuesta de Bancos
        Then Se valida la informacion del banco "<nombre>", clave "<key>", rfc "<rfc>" y nombre completo "<nombre_completo>"

        Examples: 
            |       clabe         | nombre       | key   |  rfc  |  nombre_completo |
            | 0021802122260238249 | BANAMEX      | 40002 |  " "  |       " "        |
            | 0146804271527258857 | SANTANDER    | 40014 |  " "  |       " "        |
            | 021561545094309978  | HSBC         | 40021 |  " "  |       " "        |
            | 030561545094309972  | BAJIO        | 40030 |  " "  |       " "        |
            | 036561545094309976  | INBURSA      | 40036 |  " "  |       " "        |
            | 0121806682423380297 | BBVA BANCOMER| 40012 |  " "  |       " "        |
            | 0723203093020696736 | BANORTE      | 40072 |  " "  |       " "        |
            | 1061802122260238249 | BANK OF AMERICA| 40106 |  " "  |       " "        |
            | 127561545094309979  | AZTECA       | 40127 |  " "  |       " "        |
            | 128561545094309978  | AUTOFIN      | 40128 |  " "  |       " "        |
            | 137561545094309972  | BANCOPPEL    | 40137 |  " "  |       " "        |

    Scenario: Banco no encontrado por CLABE
        Given El url "$BANK"
        And Los params enviados en la solicitud
        | key    | Value              |
        | clabe  | 0001802122260238249|
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "404"
        Then Se recibe un mensaje "No se encontro banco"

    Scenario: Banco no encontrado por Nombre
        Given El url "$BANK"
        And Los params enviados en la solicitud
        | key    | Value  |
        | nombre | Patito |
        When Se envia una solicitud GET
        Then Se valida la respuesta codigo "404"
        Then Se recibe un mensaje "No se encontro banco"
        
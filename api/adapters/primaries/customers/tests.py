"""Test for customer API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1
OPENFIN_ID = 1
IDTIPO = 1


class CustomersAPITest(BaseAPITest):
    """API for testing customer's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    # customers test
    def test_list_customers(self):
        """function for test list customes"""
        url = reverse("list-customers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # persona fisica test
    def test_detail_customers_persona_fisica(self):
        """function for test detail customer persona fisica"""
        url = "%s?user_id=%s" % (reverse("crud-customers-persona-fisica"), CUSTOMER_ID)

    def test_create_customers_persona_fisica(self):
        """function for test create customer persona fisica"""
        url = reverse("crud-customers-persona-fisica")
        data = {
            "user_id": 1,
            "openfin_info": {
                "datos_personales": {
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "fecha_nacimiento": "2000-01-01",
                    "pais_nacionalidad": "México",
                    "nacionalidad": "Mexicana",
                    "entidad_de_nacimiento": "Monterrey",
                    "genero": "nobinario",
                    "telefono": "8117480407",
                    "rfc": "1234567890123",
                    "regimen_fiscal": "un regimen fiscal",
                    "curp": "MGUE746298KFHJE6Y4",
                    "cp_fiscal": "uncp",
                    "email": "un@email.io",
                },
                "domicilio": {
                    "calle": "unacalle",
                    "numext": "unnumext",
                    "numint": "unnumint",
                    "pais": "nombredelpais",
                    "estado": "unestado",
                    "ciudad": "unacolonia",
                    "alcaldia": "unmunicipio",
                    "cp": "uncp",
                },
                "propietario_legal": {
                    "curp": "MGUE746298KFHJE6Y4",
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "fecha_nacimiento": "2000-01-01",
                    "pais_nacionalidad": "México",
                    "nacionalidad": "Mexicana",
                    "entidad_de_nacimiento": "Monterrey",
                    "genero": "hola",
                    "ocupacion": "plomero",
                    "rfc": "MGUAY27498S09",
                    "regimen_fiscal": "un regimen fiscal",
                    "cp_fiscal": "uncp",
                    "domicilio": {
                        "calle": "unacalle",
                        "numext": "unnumext",
                        "numint": "unnumint",
                        "pais": "México",
                        "estado": "unestado",
                        "ciudad": "unacolonia",
                        "alcaldia": "unmunicipio",
                        "cp": "uncp",
                    },
                    "telefono": "8117480407",
                    "email": "un@email.io",
                },
                "perfil_transaccional": {
                    "ocupacion": "plomero",
                    "giro": "drogs",
                    "actividad": "vender",
                    "ingreso_mensual_neto": "24000",
                    "fuente_de_ingreso": "soy nini",
                    "procedencia_del_recuerso": "un aca",
                    "ingresos_al_mes": "23000",
                    "operaciones_por_mes": "2",
                    "destinatarios_operaciones": "unos destinatarios",
                    "proveedores": "un proveedor",
                    "cuenta_propia": False,
                },
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_customers_persona_fisica_propietario_legal(self):
        """function for test create customer persona fisica"""
        url = reverse("crud-customers-persona-fisica")
        data = {
            "user_id": 3,
            "openfin_info": {
                "datos_personales": {
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "fecha_nacimiento": "2000-01-01",
                    "pais_nacionalidad": "México",
                    "nacionalidad": "Mexicana",
                    "entidad_de_nacimiento": "Monterrey",
                    "telefono": "8117480407",
                    "genero": "nobinario",
                    "email": "un@email.io",
                    "rfc": "1234567890123",
                    "regimen_fiscal": "un regimen fiscal",
                    "curp": "MGUE746298KFHJE6Y4",
                    "cp_fiscal": "uncp",
                },
                "domicilio": {
                    "calle": "unacalle",
                    "numext": "unnumext",
                    "numint": "unnumint",
                    "pais": "nombredelpais",
                    "estado": "unestado",
                    "ciudad": "unacolonia",
                    "alcaldia": "unmunicipio",
                    "cp": "uncp",
                },
                "perfil_transaccional": {
                    "ocupacion": "plomero",
                    "giro": "drogs",
                    "actividad": "vender",
                    "ingreso_mensual_neto": "24000",
                    "fuente_de_ingreso": "soy nini",
                    "procedencia_del_recuerso": "un aca",
                    "ingresos_al_mes": "23000",
                    "operaciones_por_mes": "2",
                    "destinatarios_operaciones": "unos destinatarios",
                    "proveedores": "un proveedor",
                    "cuenta_propia": True,
                },
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_customers_persona_fisica(self):
        """function for test update customer persona fisica"""
        url = "%s?user_id=%s" % (reverse("crud-customers-persona-fisica"), CUSTOMER_ID)
        data = {
            "user_id": 1,
            "openfin_info": {
                "datos_personales": {
                    "nombre": "MAURICIO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "fecha_nacimiento": "2000-01-01",
                    "pais_nacionalidad": "México",
                    "nacionalidad": "Mexicana",
                    "genero": "nobinario",
                    "entidad_de_nacimiento": "Monterrey",
                    "telefono": "8117480407",
                    "email": "un@email.io",
                    "rfc": "1234567890123",
                    "regimen_fiscal": "un regimen fiscal",
                    "curp": "MGUE746298KFHJE6Y4",
                    "cp_fiscal": "uncp",
                },
                "domicilio": {
                    "calle": "unacalle",
                    "numext": "unnumext",
                    "numint": "unnumint",
                    "pais": "nombredelpais",
                    "estado": "unestado",
                    "ciudad": "unacolonia",
                    "alcaldia": "unmunicipio",
                    "cp": "uncp",
                },
                "propietario_legal": {
                    "curp": "MGUE746298KFHJE6Y4",
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "fecha_nacimiento": "2000-01-01",
                    "pais_nacionalidad": "México",
                    "entidad_de_nacimiento": "Monterrey",
                    "genero": "nobinario",
                    "nacionalidad": "Mexicana",
                    "ocupacion": "plomero",
                    "rfc": "MGUAY27498S09",
                    "regimen_fiscal": "un regimen fiscal",
                    "cp_fiscal": "uncp",
                    "domicilio": {
                        "calle": "unacalle",
                        "numext": "unnumext",
                        "numint": "unnumint",
                        "pais": "México",
                        "estado": "unestado",
                        "ciudad": "unacolonia",
                        "alcaldia": "unmunicipio",
                        "cp": "uncp",
                    },
                    "telefono": "8117480407",
                    "email": "un@email.io",
                },
                "perfil_transaccional": {
                    "ocupacion": "plomero",
                    "giro": "drogs",
                    "actividad": "vender",
                    "ingreso_mensual_neto": "24000",
                    "fuente_de_ingreso": "soy nini",
                    "procedencia_del_recuerso": "un aca",
                    "ingresos_al_mes": "23000",
                    "operaciones_por_mes": "2",
                    "destinatarios_operaciones": "unos destinatarios",
                    "proveedores": "un proveedor",
                    "cuenta_propia": True,
                },
            },
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_customers_persona_fisica(self):
        """function for test create customer persona fisica"""
        url = "{}?user_id={}".format(
            reverse("crud-customers-persona-fisica"), CUSTOMER_ID
        )
        user_id = {"user_id": 1}
        response = self.client.delete(url, user_id, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # tests persona moral
    def test_detail_customers_persona_moral(self):
        """function for test detail customer persona moral"""
        url = "%s?user_id=%s" % (reverse("crud-customers-persona-moral"), CUSTOMER_ID)

    def test_create_customer_persona_moral(self):
        """function for test create customer persona moral"""
        url = reverse("crud-customers-persona-moral")
        data = {
            "user_id": 1,
            "openfin_info": {
                "datos_empresa": {
                    "razon_social": "una razon social",
                    "nacionalidad": "una nacinalidad",
                    "rfc": "123456789012",
                    "num_ser_fir_elec": "2343534235345",
                    "giro_mercantil": "un giro mercantil",
                    "cuenta_clabe": "191919191919191919",
                    "banco_cuenta_clabe": "BBVA",
                },
                "escritura_constitutiva": {
                    "fecha_constitucion": "2000-01-01",
                    "num_escritura": "666",
                    "fecha_protocolizacion": "2000-01-01",
                    "rfc": "123546576879",
                    "curp": "quw74us74us74us7",
                },
                "representante_legal": {
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "email": "postcj@io.com",
                    "num_escr_pub": "21874983",
                    "fecha_protocolizacion": "2000-01-01",
                    "firma_autografa": "una firma",
                    "clave_lada": "098762034957603786",
                    "telefono": "1234567891",
                    "extencion": "234",
                    "rfc": "1235465768791",
                    "curp": "quw74us74us74us7",
                },
                "domicilio": {
                    "calle": "unacalle",
                    "numext": "unnumext",
                    "numint": "unnumint",
                    "pais": "nombredelpais",
                    "estado": "unestado",
                    "ciudad": "unacolonia",
                    "alcaldia": "unmunicipio",
                    "cp": "uncp",
                },
                "otros_datos_personales": {
                    "numero_de_cuenta": "123412354123",
                    "clave_bancaria": "231423412435",
                    "institucion_financiera": "bbva",
                    "nombre_comercial": "un nombre comercial",
                    "actividades_y_otros": "una actividad y otros",
                    "corroborar_datos": "un corroborar datos",
                    "clave_bancaria_digitalizada": "123412452345",
                    "institucion_financiera_digitalizada": "bbvax2",
                    "firma_digitalizada": "una firma bien perrona",
                },
                "datos_de_contacto": {
                    "email": "postcj@io.com",
                    "telefono": "1234567891",
                    "razon_social": "una razon social",
                    "rfc": "asd123456789",
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                },
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_customers_persona_moral(self):
        """function for test update customer persona moral"""
        url = "{}?user_id={}".format(
            reverse("crud-customers-persona-moral"), CUSTOMER_ID
        )
        data = {
            "user_id": 1,
            "openfin_info": {
                "datos_empresa": {
                    "razon_social": "una razon social",
                    "nacionalidad": "una nacinalidad",
                    "rfc": "123456789012",
                    "num_ser_fir_elec": "2343534235345",
                    "giro_mercantil": "un giro mercantil",
                    "cuenta_clabe": "191919191919191919",
                    "banco_cuenta_clabe": "BBVA",
                },
                "escritura_constitutiva": {
                    "fecha_constitucion": "2000-01-01",
                    "num_escritura": "999",
                    "fecha_protocolizacion": "2000-01-01",
                    "rfc": "123546576879",
                    "curp": "quw74us74us74us7",
                },
                "representante_legal": {
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                    "email": "postcj@io.com",
                    "num_escr_pub": "21874983",
                    "fecha_protocolizacion": "2000-01-01",
                    "firma_autografa": "una firma",
                    "clave_lada": "098762034957603786",
                    "telefono": "1234567891",
                    "extencion": "234",
                    "rfc": "1235465768791",
                    "curp": "quw74us74us74us7",
                },
                "domicilio": {
                    "calle": "unacalle",
                    "numext": "unnumext",
                    "numint": "unnumint",
                    "pais": "nombredelpais",
                    "estado": "unestado",
                    "ciudad": "unacolonia",
                    "alcaldia": "unmunicipio",
                    "cp": "uncp",
                },
                "otros_datos_personales": {
                    "numero_de_cuenta": "123412354123",
                    "clave_bancaria": "231423412435",
                    "institucion_financiera": "bbva",
                    "nombre_comercial": "un nombre comercial",
                    "actividades_y_otros": "una actividad y otros",
                    "corroborar_datos": "un corroborar datos",
                    "clave_bancaria_digitalizada": "123412452345",
                    "institucion_financiera_digitalizada": "bbvax2",
                    "firma_digitalizada": "una firma bien perrona",
                },
                "datos_de_contacto": {
                    "email": "postcj@io.com",
                    "telefono": "1234567891",
                    "razon_social": "una razon social",
                    "rfc": "asd123456789",
                    "nombre": "MARCO",
                    "paterno": "AGUILA",
                    "materno": "MEDRANO",
                },
            },
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_customers_persona_moral(self):
        """function for test delete customer persona moral"""
        url_query_params = "{}?user_id={}".format(
            reverse("crud-customers-persona-moral"), CUSTOMER_ID
        )
        user_id = {"user_id": 1}
        response = self.client.delete(url_query_params, user_id, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

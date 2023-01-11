# Librerias Estandar
import json
from datetime import timedelta, datetime

from apps.backoffice.models.users import UserAgentModel
from compartidos.email_sender import functions

# Librerías de Terceros
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status

# Creo esta vista para usar el user agents.
# Se crea en forma de metodo para solo copiar y pegar en la clase
# vista del login.


def detect_device_login(request):
    # obtengo la informacion del usuario para guardarlo en la cookie
    username_field = get_user_model().USERNAME_FIELD
    user_info = get_user_model().objects.get(email=username_field)
    # obtencion del user agent
    user_agent_str = request.META.get("HTTP_USER_AGENT")
    mensaje = """
                    Aqui va el correo electronico
                    """
    subject = "Acceso desde un nuevo dispositivo"
    to = user_info["email"]

    # verifico si ya se ha enviado la cookie, si no hay cookie, es dispositivo nuevo
    if "new_device" not in request.COOKIES:
        functions.send_email_notification_html(subject, to, mensaje, {})
        # return Response(mensaje,status=status.HTTP_200_OK)
    # Si ya hay una cookie, pero no corresponde al usuario
    else:
        cookie_value_json = request.COOKIES["new_device"]
        cookie_value = dict(json.loads(cookie_value_json))

        # Checa si el use_info existe en el modelo y lo compara con el user que se loquea
        cookie_value_model = UserAgentModel.objects.filter(
            user_info=cookie_value["user_info"]
        )
        # si existe extrae el user_agent y lo compara
        if cookie_value_model.exists():
            if cookie_value_model.user_agent == cookie_value["user_agent"]:
                # Se actualiza la informacion de la cookie
                info_cookie = {"user_agent": user_agent_str, "user_info": user_info}
                info_cookie_serialized = json.dumps(info_cookie)

                respuesta = Response(status=status.HTTP_200_OK)
                expires = datetime.now() + timedelta(days=90)

                respuesta.set_cookie(
                    "new_device", info_cookie_serialized, expires=expires
                )
                return respuesta
            else:
                functions.send_email_notification_html(subject, to, mensaje, {})
                # return Response(mensaje, status=status.HTTP_200_OK)
        # Si no existe, es por que nisiquiera hay usuario, pero eso ya se valido antes

from datetime import datetime
from urllib.parse import quote

class RecoveryPasswordMessages:
    def __init__(self):
        self.timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def forgot_password_message(self, usuario, url):
        url_encoded = quote(url, safe=':/?=&')

        base,email=url.split('&')
        asunto = f"Solicitud de recuperación de contraseña {self.timestamp_str}"
        mensaje = f"""
                Hola, {usuario}.
                Has solicitado recuperar la contraseña de la cuenta {email} en el portal de DYP. Para esto, hemos generado un enlace provisional.

                Enlace temporal para realizar la recuperación de la contraseña:
                {base}&{email}

                ¿No reconoces esta actividad?
                Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.

                El Equipo DyP.
                """

        return {"asunto": asunto, "mensaje": mensaje}

    def recovery_code(self, usuario, codigo):
        asunto = f"Codigo de recuperación de contraseña {self.timestamp_str}"
        mensaje = f"""
                Hola, {usuario}.
                Has solicitado recuperar la contraseña de la cuenta [correo] en el portal de DYP. Para esto, hemos generado un codigo.

                {codigo}

                ¿No reconoces esta actividad?
                Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.

                El Equipo DyP.
                """
        return {"asunto": asunto, "mensaje": mensaje}

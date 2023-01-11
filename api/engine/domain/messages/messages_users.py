from datetime import datetime

class AuthenticationMessages:

    def __init__(self):
        self.timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def temporal_blocking_message(self, usuario, correo):
        asunto = f"Bloqueo temporal de cuenta {self.timestamp_str}"
        mensaje = f"""
                Hola, {usuario}.

                La cuenta de operador {correo} ha sido bloqueada de manera temporal por rebasar el número intentos de login en el portal DyP.
                
                ¿No reconoces esta actividad?
                Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.
                
                El Equipo DyP
                """
        return {"asunto": asunto, "mensaje": mensaje}

    def permanent_blocking_message(self, usuario, correo):
        asunto = f"Bloqueo permanente de cuenta {self.timestamp_str}"
        mensaje = f"""
                        Hola, {usuario}.

                        La cuenta de operador {correo} ha sido bloqueada de manera permanente por exceder el número de intentos de ingreso en el portal DyP. Si deseas reactivar tu cuenta por favor comunícate a nuestro Centro de Atención a Usuarios.
                        
                        ¿No reconoces esta actividad?
                        Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.
                        
                        El Equipo DyP.

                        """
        return {"asunto": asunto, "mensaje": mensaje}
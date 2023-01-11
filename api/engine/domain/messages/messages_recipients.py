from datetime import datetime

class RecipientMessages:
    def __init__(self):
        self.timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def new_recipient_message(self, usuario, correo, destinatario):

        asunto = f"Nuevo destinatario {self.timestamp_str}"
        mensaje = f"""
                Hola, {usuario}.

                Se ha realizado de forma exitosa el alta de un nuevo destinatario en la cuenta {correo} con la siguiente información:
                
                Nuevo destinatario:
                {destinatario}.
                
                ¿No reconoces esta actividad?
                Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.
                
                El Equipo DyP.
                """
        return {"asunto": asunto, "mensaje": mensaje}

    def inactivate_recipient_message(self, usuario, correo, destinatario):

        asunto = f"Baja de destinatario {self.timestamp_str}"
        mensaje = f"""
                        Hola, {usuario}.

                        Se ha realizado de forma exitosa la baja del destinatario en la cuenta {correo} con la siguiente información:
                        
                        Baja de destinatario:
                        {destinatario}.
                        
                        ¿No reconoces esta actividad?
                        Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.
                        
                        El Equipo DyP.
                        """
        return {"asunto": asunto, "mensaje": mensaje}

    def activate_recipient_message(self, usuario, correo, destinatario):
        asunto = f"Reactivación de destinatario {self.timestamp_str}"
        mensaje = f"""
                        Hola, {usuario}.
                        
                        Se ha realizado de forma exitosa la reactivación del destinatario en la cuenta {correo} con la siguiente información:
                        
                        Reactivación de destinatario:
                        {destinatario}.
                        
                        ¿No reconoces esta actividad?
                        Puedes hacer caso omiso a este correo o comunicarte al centro de atención a usuarios DyP para cualquier aclaración.
                        
                        El Equipo DyP.
                        """
        return {"asunto": asunto, "mensaje": mensaje}


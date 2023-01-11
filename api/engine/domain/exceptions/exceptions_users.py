from compartidos.exceptions import ExceptionBase
from rest_framework.exceptions import AuthenticationFailed


class UserDoesNotExist(ExceptionBase):
    """Customer does not exist"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = {"detail": f"Customer {self.user_id} does not exist"}
        super().__init__()


class UserEmailDoesNotExist(ExceptionBase):
    """Customer does not exist"""

    def __init__(self, email: str):
        self.email = email
        self.message = {"detail": f"Customer {self.email} does not exist"}
        super().__init__()


class NoEmailregistered(ExceptionBase):
    msg = "Este correo no está registrado, ¿Deseas registrarte?"

    def __init__(self):
        self.message = {"detail": NoEmailregistered.msg}
        super().__init__()


class BlockedAccount(ExceptionBase):
    msg = "Por seguridad tu cuenta ha sido bloqueada, intenta de nuevo en 10 minutos a partir de este momento."

    def __init__(self):
        self.message = {"detail": BlockedAccount.msg}
        super().__init__()


class UserManySessions(ExceptionBase):
    msg = "Actualmente ya cuentas con una sesión abierta,para poder iniciar una nueva asegurate de cerrar la anterior."

    def __init__(self):
        self.message = {"detail": UserManySessions.msg}
        super().__init__()


class InvalidPassword(ExceptionBase):
    """Invalid password"""

    msg = "La contraseña o token son incorrectos, después de 3 intentos tu cuenta será bloqueada."

    def __init__(self):
        self.message = {"detail": InvalidPassword.msg}
        super().__init__()


class AccountBlockedAdmin(ExceptionBase):
    """Invalid password"""

    msg = """Por seguridad tu cuenta ha sido bloqueada. Para poder acceder nuevamente comunicate con el Centro de Atención a Usuarios DyP:
800 110 90 90
En horario de atención: Lunes a viernes de 08:00 a 20:00 horas, sábados de 08:00 a 15:00 horas.
O escribenos a: clientes@depositosypagos.com"""

    def __init__(self):
        self.message = {"detail": AccountBlockedAdmin.msg}
        super().__init__()


class UserInactive(ExceptionBase):
    """User is innactive"""

    msg = """Tu cuenta se encuentra Inactiva. 
    Para poder acceder nuevamente comunicate con el Centro de Atención a Usuarios DyP:
    800 110 90 90
    En horario de atención: 
    Lunes a viernes de 08:00 a 20:00 horas, sábados de 08:00 a 15:00 horas.
    O escribenos a: clientes@depositosypagos.com"""

    def __init__(self):
        self.message = {"detail": UserInactive.msg}
        super().__init__()


class UserAlreadyExists(ExceptionBase):
    """Customer already exist"""

    def __init__(self, email: str):
        self.email = email
        self.message = {
            "detail": f"email: {self.email} is already assigned to another customer"
        }
        super().__init__()


class InvalidLocation(ExceptionBase):
    """Invalid location (MSG20)"""

    def __init__(self):
        self.message = {
            "detail": "Por disposición Oficial requerimos acceder a tu ubicación geográfica. La "
            "información que nos proporciones no se utilizará para ningún otro "
            "propósito.\n¿Cómo compartir tu ubicación geográfica?\nConsulta en el menú de tu "
            "navegador con la opción Configuración y selecciona Compartir ubicación.\nRecuerda "
            "autorizar el dispositivo (computadora tablet) que uses para ingresar a DyP para "
            "Compartir ubicación.\nTe sugerimos volver a cargar la página actual para que se "
            "aplique correctamente la autorización de tu ubicación geográfica."
        }
        super().__init__()


class ValidLocation(ExceptionBase):
    """Valid location (MSG18)"""

    def __init__(self):
        self.message = {
            "detail": "Tu cuenta se encuentra en proceso de validación.\nNuestro equipo te informará "
            "cuando concluya el proceso y puedas usar tu cuenta."
        }
        super().__init__()


class PasswordNotMatch(ExceptionBase):
    """Passswords do not match (MSG10)"""

    def __init__(self):
        self.message = {
            "detail": "Las contraseñas no coinciden, asegurate de ingresar las mismas."
        }
        super().__init__()

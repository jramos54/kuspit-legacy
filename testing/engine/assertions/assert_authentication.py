import jwt
import time

class TokenAssertion:
    def __init__(self, access, refresh, logger):
        self.access = access
        self.refresh = refresh
        self.logger = logger
        self.assertion_access_result = self.assertion_access()
        self.assertion_refresh_result = self.assertion_refresh()

    def assertion_access(self):
        result = bool(self.access)
        if result:
            self.logger.assert_pass("El access token existe")
        else:
            self.logger.assert_fail("El access token no existe")
        return result

    def assertion_refresh(self):
        result = bool(self.refresh)
        if result:
            self.logger.assert_pass("El refresh token existe")
        else:
            self.logger.assert_fail("El refresh token no existe")
        return result
    
    def get_expiration_time(self, token):
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            exp_time = decoded_token.get('exp', 0)
            exp_time_ms = exp_time * 1000
            return exp_time_ms
        except jwt.ExpiredSignatureError:
            self.logger.error("El token ha expirado")
            return 0
        except Exception as e:
            self.logger.error(f"Error al decodificar el token: {e}")
            return 0

    def get_time_minutes(self, token):
        milliseconds = self.get_expiration_time(token)
        minutes = (milliseconds / 1000) / 60
        return max(0, minutes)
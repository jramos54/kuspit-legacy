import requests
from testing.common.logger_testing import Logger

logger=Logger("HTTPHelper")


class HTTPClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url,accessToken,*args,**kwargs):
        """Envía una solicitud GET a la URL especificada con parámetros opcionales."""
        if accessToken:
            headers = {
                'Authorization': 'Bearer '+accessToken
                }
            req = requests.Request('GET', url, headers=headers, params=kwargs)
            prepared = self.session.prepare_request(req)
            
            logger.warning(f"URL completa: {prepared.url}")
            
            # Enviar la solicitud GET con la URL preparada
            response = self.session.send(prepared)
            return response
        else:
            
            req = requests.Request('GET', url, params=kwargs)
            prepared = self.session.prepare_request(req)
            
            logger.warning(f"URL completa: {prepared.url}")
            
            # Enviar la solicitud GET con la URL preparada
            response = self.session.send(prepared)
            return response

    def post(self, url, payload=None,accessToken=None,*args, **kwargs):
        """Envía una solicitud POST a la URL especificada con un payload opcional."""
        if accessToken:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+accessToken

                }
            response = self.session.post(url, headers=headers, data=payload)
            return response
        else:
            headers = {
                'Content-Type': 'application/json',
                }
            response = self.session.post(url, headers=headers, data=payload)
            return response

    def put(self, url,accessToken=None, payload=None,*args, **kwargs):
        """Envía una solicitud PUT a la URL especificada con un payload opcional."""
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+accessToken

                }

        logger.warning(payload)
        req = requests.Request('PUT', url, headers=headers, params=kwargs,json=payload)
        prepared = self.session.prepare_request(req)
        
        logger.warning(f"URL completa: {prepared.url}")
        
        # Enviar la solicitud PATCH con la URL preparada
        response = self.session.send(prepared)
        return response


    def patch(self, url,accessToken=None, payload=None,*args, **kwargs):
        """Envía una solicitud PATCH a la URL especificada con un payload opcional."""
        if accessToken:
            headers = {
                'Authorization': 'Bearer '+ accessToken
                }
            
            req = requests.Request('PATCH', url, headers=headers, params=kwargs,json=payload)
            prepared = self.session.prepare_request(req)
            
            logger.warning(f"URL completa: {prepared.url}")
            
            # Enviar la solicitud PATCH con la URL preparada
            response = self.session.send(prepared)
            return response
        else:
            req = requests.Request('PATCH', url,params=kwargs,json=payload)
            prepared = self.session.prepare_request(req)
            
            logger.warning(f"URL completa: {prepared.url}")
            
            # Enviar la solicitud PATCH con la URL preparada
            response = self.session.send(prepared)
            return response


    def delete(self, url, params=None, payload=None):
        """Envía una solicitud DELETE a la URL especificada con parámetros y payload opcionales."""
        response = self.session.delete(url, params=params, json=payload)
        return response

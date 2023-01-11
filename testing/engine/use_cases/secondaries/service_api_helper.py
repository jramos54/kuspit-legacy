from testing.adapters.secondaries.HTTPHelper import HTTPClient
from testing.common.logger_testing import Logger

logger=Logger("Api helper")


class APIHelper:
    def __init__(self) -> None:
        self.client=HTTPClient()
        self.response=None
        
    def post_request(self,url,payload,accessToken=None,*args, **kwargs):
        self.response = self.client.post(url,payload,accessToken)
        # logger.info(f"respuesta de API {self.response.json()}")
        
    def get_request(self,url,accessToken,*args, **kwargs):
        self.response = self.client.get(url,accessToken,**kwargs)
        # logger.info(f"respuesta de API {self.response.json()}")
    
    def put_request(self,url,accessToken=None,payload=None,*args, **kwargs):
        self.response = self.client.put(url=url,accessToken=accessToken,payload=payload)
     
    def patch_request(self,url,accessToken,*args, **kwargs):
        self.response = self.client.patch(url,accessToken,**kwargs)
        # logger.info(f"respuesta de API {self.response.json()}")
        
    def get_response(self):
        return self.response.json()
    
    def get_response_code(self):
        return self.response.status_code
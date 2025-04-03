import requests
from typing import Optional

class SimpleAPIClient:
    
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint:str, headers:Optional[dict] = None, **params):
        
        try:
            with requests.get(self.base_url+endpoint, params=params, headers=headers) as response:
                response.raise_for_status()  # levanta HTTPError para códigos 4xx/5xx
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro na requisição: {e}")

        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise ValueError("Resposta não está em formato JSON")

        return response.json()

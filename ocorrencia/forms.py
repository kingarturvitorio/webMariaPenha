import requests
from django import forms

# URL da API para buscar as categorias
CATEGORIAS_API_URL = "http://3.20.168.85/api/v1/solicitantes/"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDM5NDY5MzkxLCJpYXQiOjE3MjQxMDkzOTEsImp0aSI6IjkzMjQ2ZGFlMTYyNjQ3MjJiNDNjNTg5ZjkzMGE2ZDdmIiwidXNlcl9pZCI6MX0.02gNxQL4v1RPRCA_Gwfkuf0G0vVI4axYQYoTekuJ7Z0"  # Substitua pelo token correto ou obtenha dinamicamente

class Ocorrencias(forms.Form):

    nivelocorrencia = forms.CharField(max_length=100)
    categoria = forms.ChoiceField(choices=[], label="Categoria")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cabeçalhos com o Bearer Token
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Faça a requisição para a API para obter as categorias
        response = requests.get(CATEGORIAS_API_URL, headers=headers)

        if response.status_code == 200:
            categorias = response.json()

            # Mapear as categorias para o formato (id, nome) que o ChoiceField espera
            choices = [(categoria['id'], categoria['solicitante']) for categoria in categorias]

            # Defina as opções do campo "categoria"
            self.fields['categoria'].choices = choices
        else:
            # Caso haja erro, defina como uma lista vazia ou exiba uma mensagem de erro
            self.fields['categoria'].choices = []
            self.fields['categoria'].widget.attrs['disabled'] = 'disabled'
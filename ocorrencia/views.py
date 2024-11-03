import requests
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from ocorrencia.forms import Ocorrencias

API_URL = "http://3.20.168.85/api/v1/ocorrencias/"  # Substitua pela URL da API

class OcorrenciaListView(ListView):
    template_name = 'listar_ocorrencia.html'
    context_object_name = 'ocorrencias'


    # Mapeamento de prioridades para ordenação
    prioridade_mapping = {
        '1': 3, #Baixo
        '2': 2, #Média
        '3': 1  #Alta
    }


    def get_queryset(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDM5NDY5MzkxLCJpYXQiOjE3MjQxMDkzOTEsImp0aSI6IjkzMjQ2ZGFlMTYyNjQ3MjJiNDNjNTg5ZjkzMGE2ZDdmIiwidXNlcl9pZCI6MX0.02gNxQL4v1RPRCA_Gwfkuf0G0vVI4axYQYoTekuJ7Z0',  # Inclua o token ou qualquer outro header necessário
            'Content-Type': 'application/json'  # Dependendo da API, isso pode ser opcional
        }
        # Fazendo a requisição GET para a API
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # Obtém os dados da API
            ocorrencias = response.json()

            # Ordenando as ocorrências manualmente com base na prioridade e data
            ocorrencias.sort(key=lambda x: (self.prioridade_mapping.get(x['nivelocorrencia'], 4), x['datahora']), reverse=True)

            # Substituindo vírgulas por pontos nas coordenadas e convertendo para float
            for ocorrencia in ocorrencias:
                ocorrencia['latocorr'] = float(str(ocorrencia['latocorr']).replace(',', '.'))
                ocorrencia['longocorr'] = float(str(ocorrencia['longocorr']).replace(',', '.'))
                # Se a API retornar o ID do solicitante, você pode fazer outra requisição para obter os dados do solicitante
                solicitante_id = ocorrencia.get('solicitante')  # Supondo que o JSON retorna isso
                solicitante_response = requests.get(f"http://3.20.168.85/api/v1/solicitantes/{solicitante_id}/", headers=headers)
                if solicitante_response.status_code == 200:
                    solicitante_data = solicitante_response.json()
                    ocorrencia['solicitante_nome'] = solicitante_data.get('nome')  # Adiciona o nome do solicitante ao dicionário

            return ocorrencias
        else:
            return []  # Se houver erro na API, retorna uma lista vazia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Para cada ocorrência, definimos uma classe CSS com base na prioridade
        for obj in context['ocorrencias']:
            if obj['nivelocorrencia'] == 1:
                obj['css_class'] = 'bg-lightgreen'
            elif obj['nivelocorrencia'] == 2:
                obj['css_class'] = 'bg-lightyellow'
            else:  # Para prioridade 'ALTA'
                obj['css_class'] = 'bg-lightred'

        return context

        

class OcorrenciaTabelaListView(ListView):

    template_name = 'ocorrencia.html'
    context_object_name = 'ocorrencias'

    def get_queryset(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDM5NDY5MzkxLCJpYXQiOjE3MjQxMDkzOTEsImp0aSI6IjkzMjQ2ZGFlMTYyNjQ3MjJiNDNjNTg5ZjkzMGE2ZDdmIiwidXNlcl9pZCI6MX0.02gNxQL4v1RPRCA_Gwfkuf0G0vVI4axYQYoTekuJ7Z0',  # Inclua o token ou qualquer outro header necessário
            'Content-Type': 'application/json'  # Dependendo da API, isso pode ser opcional
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []  # Retorne uma lista vazia ou lide com o erro de outra maneira
        
class OcorrenciaCreate(CreateView):
    login_url = reverse_lazy('login')
    form_class = Ocorrencias
    template_name = 'form.html'
    success_url = reverse_lazy('ocorrencia-list')

    def form_valid(self, form):
        data = form.cleaned_data  # Dados que serão enviados no POST
        headers = {
            'Authorization': 'Bearer seu_token_aqui',  # Substitua com seu token ou outra autenticação
            'Content-Type': 'application/json'  # Dependendo da API
        }
        response = requests.post(API_URL, json=data, headers=headers)

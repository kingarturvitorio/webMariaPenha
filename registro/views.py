import requests
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from ocorrencia.forms import Ocorrencias
from .forms import RegistroForm
from datetime import date
from .models import Registro
from ocorrencia.models import Ocorrencia
from django.http import Http404, HttpResponseRedirect
import logging

API_URL = "http://3.20.168.85/api/v1/solicitantes/"  # Substitua pela URL da API

class Registro1:
    def __init__(self, data):
        self.id = data.get('id')  # Supondo que 'id' seja o identificador vindo da API
        self.status = data.get('status')
        self.nome = data.get('nome')
        self.cpf = data.get('cpf')
        self.telefone = data.get('telefone')
        self.logradouro = data.get('logradouro')
        self.nres = data.get('nres')
        self.bairro = data.get('bairro')
        self.cidade = data.get('cidade')
        self.uf = data.get('uf')
        self.cep = data.get('cep')
        self.dtnasc = data.get('dtnasc')
        self.dtcadastro = data.get('dtcadastro')
        self.processo = data.get('processo')
        self.observacoes = data.get('observacoes')
        self.descricao_ocorrencia = data.get('descricao_ocorrencia')
    def __str__(self):
        return f"{self.nome} ({self.id})"
    
class RegistroTabelaListView(ListView):
    template_name = 'registro.html'
    context_object_name = 'registros'

    def get_queryset(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',  # Inclua o token ou qualquer outro header necessário
            'Content-Type': 'application/json'  # Dependendo da API, isso pode ser opcional
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            registros = [Registro1(item) for item in data]  # Converta os dados da API em objetos Registro
            return registros
        else:
            return []  # Retorne uma lista vazia se houver erro
        
class RegistroCreateView(CreateView):
    login_url = reverse_lazy('login')
    form_class = RegistroForm
    template_name = 'form.html'
    success_url = reverse_lazy('ocorrencia-list')

    def form_valid(self, form):
        data = form.cleaned_data  # Dados limpos do formulário
        
        # Convertendo campos de data para string no formato 'YYYY-MM-DD'
        if isinstance(data.get('dtnasc'), date):
            data['dtnasc'] = data['dtnasc'].isoformat()
        if isinstance(data.get('dtcadastro'), date):
            data['dtcadastro'] = data['dtcadastro'].isoformat()

        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',  # Substitua com seu token ou outra autenticação
            'Content-Type': 'application/json'  # Dependendo da API
        }

        # Enviando os dados como JSON
        response = requests.post(API_URL, json=data, headers=headers)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 201:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Erro ao tentar criar o registro.')
            return self.form_invalid(form)
        
class RegistroUpdateView(UpdateView):
    login_url = reverse_lazy('login')
    form_class = RegistroForm
    template_name = 'form.html'
    success_url = reverse_lazy('ocorrencia-list')
    registro_bloqueado = False  # Inicializamos a flag como False

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"http://3.20.168.85/api/v1/solicitantes/{id}/", headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Obtem o CPF do solicitante
            cpf = data.get("cpf")
            print(cpf)
            if not cpf:
                raise ValueError("CPF do solicitante não encontrado.")

            # Verifica na API de ocorrências se há uma ocorrência associada a este CPF
            response_ocorrencia = requests.get(f"http://3.20.168.85/api/v1/ocorrencias/?cpf_solicitante={cpf}", headers=headers)
            if response_ocorrencia.status_code == 200:
                ocorrencias = response_ocorrencia.json()

                # Se há ocorrências associadas ao solicitante, bloqueia a atualização
                if ocorrencias:
                    raise ValueError("Este registro não pode ser alterado pois está vinculado a uma ocorrência.")

            # Filtra apenas os campos válidos do modelo Registro
            registro_data = {key: data[key] for key in data if key in [field.name for field in Registro._meta.fields]}

            # Encontra ou cria um registro localmente com os dados da API
            registro, created = Registro.objects.update_or_create(id=data['id'], defaults=registro_data)

            return registro
        else:
            raise Http404("Registro não encontrado")

    def get_initial(self):
            # Pegue os dados do objeto (retornado pelo get_object)
            registro = self.get_object()
            # Retorna os dados para inicializar o formulário
            return {
                'status': registro.status,
                'nome': registro.nome,
                'cpf': registro.cpf,
                'telefone': registro.telefone,
                'logradouro': registro.logradouro,
                'nres': registro.nres,
                'bairro': registro.bairro,
                'cidade': registro.cidade,
                'uf': registro.uf,
                'cep': registro.cep,
                'dtnasc': registro.dtnasc,
                'dtcadastro': registro.dtcadastro,
                'processo': registro.processo,
                'observacoes': registro.observacoes,
                'descricao_ocorrencia': registro.descricao_ocorrencia,
            }

    def form_valid(self, form):
        data = form.cleaned_data  # Dados limpos do formulário
        id = self.kwargs.get('id')  # Pegue o ID da URL

        # Convertendo campos de data para string no formato 'YYYY-MM-DD'
        if isinstance(data.get('dtnasc'), date):
            data['dtnasc'] = data['dtnasc'].isoformat()
        if isinstance(data.get('dtcadastro'), date):
            data['dtcadastro'] = data['dtcadastro'].isoformat()

        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',  # Substitua com seu token ou outra autenticação
            'Content-Type': 'application/json'  # Dependendo da API
        }

        # Enviando os dados como JSON
        response = requests.put(f"http://3.20.168.85/api/v1/solicitantes/{id}/", json=data, headers=headers)  # Use PUT para atualização

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:  # Geralmente, o status para uma atualização bem-sucedida é 200
            return super().form_valid(form)
        else:
            form.add_error(None, 'Erro ao tentar atualizar o registro.')
            return self.form_invalid(form)
# Configurando o logger
logger = logging.getLogger(__name__)

class RegistroDeleteView(DeleteView):
    login_url = reverse_lazy('login')
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('ocorrencia-list')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')  # Obtém o ID da URL
        print(id)  # Isso ajudará a ver o ID que está sendo passado
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',  # Substitua com seu token ou outra autenticação
            'Content-Type': 'application/json'  # Dependendo da API
        }

        # Enviando os dados como JSON
        response = requests.get(f"http://3.20.168.85/api/v1/solicitantes/{id}/", headers=headers)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            # Cria um objeto Registro apenas para exibição (opcional)
            return Registro1(data)
        else:
            raise Http404("Registro não encontrado")

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            id = self.object.id  # ID do registro a ser excluído
            print(id)  # Isso ajudará a ver o ID que está sendo passado

            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ0MDYzOTE1LCJpYXQiOjE3Mjg3MDM5MTUsImp0aSI6IjllMWYxODgzOGIxNjRiZGNiNDg2MDdlNDc3YjRkNGVkIiwidXNlcl9pZCI6MX0.wY782l5Mke0w7BiOrodYRJA7CMwRISVk5kW1Q9CvXv4',  # Substitua com seu token ou outra autenticação
                'Content-Type': 'application/json'  # Dependendo da API
            }

            # Fazendo a requisição DELETE para a API
            response = requests.delete(f"http://3.20.168.85/api/v1/solicitantes/{id}/", headers=headers)
            # Log da resposta da API
            logger.info(f"Delete Response Status Code: {response.status_code}")
            logger.info(f"Delete Response Body: {response.text}")
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 204:  # 204 No Content indica sucesso na exclusão
                 return HttpResponseRedirect(self.success_url)  # Redireciona para a URL de sucesso
            else:
                # Log de erro se a exclusão falhar
                # logger.error(f"Erro ao excluir registro {id}: {response.text}")
                return self.form_invalid(None) 
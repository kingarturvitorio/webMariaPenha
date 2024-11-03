from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = [
            'nome', 'cpf', 'telefone', 'logradouro', 'nres', 'bairro', 'cidade',
            'uf', 'cep', 'dtnasc', 'dtcadastro', 'processo', 'observacoes', 'status', 'password', 'descricao_ocorrencia'
        ]
        widgets = {
            'password': forms.PasswordInput(),  # Campo para senha com input de senha
        }
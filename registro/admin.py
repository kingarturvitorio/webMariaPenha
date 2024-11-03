from django.contrib import admin

# Register your models here.
from registro.models import Registro

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'telefone', 'logradouro', 'nres', 'bairro', 'cidade',
            'uf', 'cep', 'dtnasc', 'dtcadastro', 'processo', 'observacoes', 'status', 'password', 'descricao_ocorrencia')
    search_fields = ('nome',)


admin.site.register(Registro, RegistroAdmin)
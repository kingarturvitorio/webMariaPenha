from django.contrib import admin

# Register your models here.
from ocorrencia.models import Ocorrencia

class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('descricao_ocorrencia', 'prioridade', 'data', 'boletim_ocorrencia', 'numero_registro_justica', 'foto_ocorrencia', 'registro')
    search_fields = ('prioridade',)

admin.site.register(Ocorrencia, OcorrenciaAdmin)
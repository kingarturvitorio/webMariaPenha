from django.db import models
from datetime import datetime
from registro.models import Registro

class Ocorrencia(models.Model):

    OPCOES_PRIORIDADE = [
        ("BAIXA","Baixa"),
        ("MEDIA","Media"),
        ("Alta","Alta"),
    ]

    descricao_ocorrencia = models.TextField(null=False, blank=False)
    prioridade = models.CharField(max_length=100, choices=OPCOES_PRIORIDADE, default='')
    data = models.DateTimeField(default=datetime.now, blank=True)
    boletim_ocorrencia = models.TextField(null=False, blank=False)
    numero_registro_justica = models.TextField(null=False, blank=False)
    foto_ocorrencia = models.ImageField(upload_to='ocorrencias/', blank=True, null=True)
    registro = models.ForeignKey(Registro, on_delete=models.PROTECT, related_name='registro')

    def __str__(self):
        return self.boletim_ocorrencia if self.boletim_ocorrencia else "Sem Descrição"
    
    
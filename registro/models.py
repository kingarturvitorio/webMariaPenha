from django.db import models
from django.contrib.auth.hashers import make_password

class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    nres = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=30, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    dtnasc = models.DateField(null=True, blank=True)
    dtcadastro = models.DateField(null=True, blank=True)
    processo = models.CharField(max_length=30, null=True, blank=True)
    observacoes = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=128)  # Tamanho ajustado para hash
    descricao_ocorrencia = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ao salvar, garanta que a senha seja armazenada como hash
        if self.password and not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super(Registro, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{(self.nome) (self.id)}"
    

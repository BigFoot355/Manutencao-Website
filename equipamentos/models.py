from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localtime

# Tabela de Técnicos
class Tecnico(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

# Tabela de Equipamentos
class Equipamento(models.Model):
    TIPO_UTILIZADOR = [
        ("professor", "Professor"),
        ("aluno", "Aluno"),
        ("outro", "Outro"),
    ]

    STATUS_CHOICES = [
        ("Recebido", "Recebido"),
        ("Em Reparacao", "Em Reparação"),        
        ("Em Orcamentacao", "Em Orçamentação"),
        ("Reparado", "Reparado"),
        ("Entregue", "Entregue"),
    ]

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    tipo = models.CharField(max_length=10, choices=TIPO_UTILIZADOR)
    equipamento = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=50)
    problema = models.TextField()
    outro_equipamento_entregue = models.CharField(max_length=100, default="Carregador")
    password = models.CharField(max_length=50, default="Não Tem")
    permite_abrir_pc = models.BooleanField(default=True)
    permite_apagar_dados = models.BooleanField(default=True)
    data_recepcao = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Recebido")    
    apagado = models.BooleanField(default=False)  # Flag para marcar como "apagado"
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_equipamentos")
    #created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_equipamentos")
    #updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.equipamento} ({self.numero_serie})"

# Tabela de Intervenções
class Intervencao(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    #tecnico = models.ForeignKey('auth.User', on_delete=models.CASCADE)    
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    apagado = models.BooleanField(default=False) 

    def duracao(self):
        """Retorna a duração em minutos"""
        if self.hora_inicio and self.hora_fim:
            diff = localtime(self.hora_fim) - localtime(self.hora_inicio)
            minutos = int(diff.total_seconds() // 60)
            return f"{minutos} minutos" if minutos > 0 else "Menos de 1 minuto"
        return "-"
    
    descricao = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_intervencoes")
    #created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_intervencoes")
    #updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Intervenção {self.equipamento} - {self.tecnico}"

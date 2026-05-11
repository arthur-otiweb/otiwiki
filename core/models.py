from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True)
    informacoes_gerais = models.TextField(blank=True, help_text="Servidores, metodologias, contatos, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Topico(models.Model):
    TIPO_CHOICES = [
        ('info', 'Informação Geral'),
        ('tutorial', 'Tutorial/Passo a Passo'),
        ('suporte', 'Procedimento de Suporte'),
    ]
    
    titulo = models.CharField(max_length=300)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='info')
    conteudo = models.TextField(help_text="Aceita HTML para formatação avançada")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='topicos')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topicos_criados')
    ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topicos_editados', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.titulo}"
    
    class Meta:
        ordering = ['-updated_at']

class MidiaTopico(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='midias')
    arquivo = models.FileField(upload_to='topicos/%Y/%m/%d/')
    tipo = models.CharField(max_length=10, choices=[('img', 'Imagem'), ('video', 'Vídeo')])
    descricao = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mídia para {self.topico.titulo}"

class MensagemChat(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.usuario.username}: {self.mensagem[:50]}"
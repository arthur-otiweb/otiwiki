from django.contrib import admin
from .models import Cliente, Topico, MidiaTopico, MensagemChat

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'created_at')
    search_fields = ('nome',)

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'tipo', 'autor', 'created_at')
    list_filter = ('tipo', 'cliente')
    search_fields = ('titulo', 'conteudo')

@admin.register(MidiaTopico)
class MidiaTopicoAdmin(admin.ModelAdmin):
    list_display = ('topico', 'tipo', 'descricao')

@admin.register(MensagemChat)
class MensagemChatAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensagem', 'timestamp')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import Cliente, Topico, MidiaTopico
from django.core.paginator import Paginator

@login_required
def home(request):
    ultimos_adicionados = Topico.objects.all().order_by('-created_at')[:10]
    ultimos_alterados = Topico.objects.all().order_by('-updated_at')[:10]
    
    return render(request, 'home.html', {
        'ultimos_adicionados': ultimos_adicionados,
        'ultimos_alterados': ultimos_alterados,
        'clientes': Cliente.objects.all()
    })

@login_required
def cliente_topicos(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    topicos = cliente.topicos.all()
    
    return render(request, 'topic_list.html', {
        'cliente': cliente,
        'topicos': topicos
    })

@staff_member_required
def criar_topico(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        topico = Topico.objects.create(
            titulo=request.POST['titulo'],
            tipo=request.POST['tipo'],
            conteudo=request.POST['conteudo'],
            cliente=cliente,
            autor=request.user,
            ultimo_editor=request.user
        )
        
        # Upload de múltiplas mídias
        for arquivo in request.FILES.getlist('midias'):
            tipo = 'img' if arquivo.content_type.startswith('image') else 'video'
            MidiaTopico.objects.create(
                topico=topico,
                arquivo=arquivo,
                tipo=tipo,
                descricao=request.POST.get(f'desc_{arquivo.name}', '')
            )
        
        return redirect('detalhe_topico', topico_id=topico.id)
    
    return render(request, 'criar_topico.html', {'cliente': cliente})
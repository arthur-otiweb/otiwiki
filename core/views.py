from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from .models import Cliente, Topico, MidiaTopico

@login_required
def home(request):
    ultimos_adicionados = Topico.objects.all().order_by('-created_at')[:10]
    ultimos_alterados = Topico.objects.all().order_by('-updated_at')[:10]
    clientes = Cliente.objects.all()
    
    return render(request, 'home.html', {
        'ultimos_adicionados': ultimos_adicionados,
        'ultimos_alterados': ultimos_alterados,
        'clientes': clientes
    })

@login_required
def cliente_topicos(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    topicos = cliente.topicos.all()
    
    return render(request, 'cliente_topicos.html', {
        'cliente': cliente,
        'topicos': topicos
    })

@login_required
def topico_detalhe(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    return render(request, 'topico_detalhe.html', {'topico': topico})

@staff_member_required
def topico_criar(request, cliente_id):
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
        
        # Upload de arquivos
        for arquivo in request.FILES.getlist('midias'):
            tipo = 'img' if arquivo.content_type.startswith('image') else 'video'
            MidiaTopico.objects.create(
                topico=topico,
                arquivo=arquivo,
                tipo=tipo,
                descricao=request.POST.get(f'desc_{arquivo.name}', '')
            )
        
        return redirect('topico_detalhe', topico_id=topico.id)
    
    return render(request, 'topico_form.html', {'cliente': cliente})

@staff_member_required
def topico_editar(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    
    if request.method == 'POST':
        topico.titulo = request.POST['titulo']
        topico.tipo = request.POST['tipo']
        topico.conteudo = request.POST['conteudo']
        topico.ultimo_editor = request.user
        topico.save()
        return redirect('topico_detalhe', topico_id=topico.id)
    
    return render(request, 'topico_form.html', {'topico': topico, 'cliente': topico.cliente})
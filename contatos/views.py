from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    # organiza os contatos por id em ordem decrescente. Mostrar=True para mostrar os não ocultos.
    contatos = Contato.objects.order_by('-id').filter(mostrar=True)

    # mostra 10 contatos por página
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        #   Key      Value
        'contatos': contatos
    })


def ver_contato(request, contato_id):
    # levanta um erro 404 quando a página não for encontrada
    contato = get_object_or_404(Contato, id=contato_id)

    # Caso o contato esteja oculto, mesmo ele existindo na base de dados, levantará um erro 404.
    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        #   Key      Value
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'Campo pesquisa não pode ficar vazio.')
        return redirect('index')

    campos = Concat('nome', Value(' '),'sobrenome')

    # Filtro de pesquisa de contatos por nome, sobrenome e nome completo.
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo))

    # mostra 10 contatos por página
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        #   Key      Value
        'contatos': contatos
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from .models import Contato


def index(request):    
    # contatos = Contato.objects.all()
    # contatos = Contato.objects.order_by('nome') # crescente
    # contatos = Contato.objects.order_by('-nome') # decrescente
    contatos = Contato.objects.order_by(  # ordena
        "-id"
    ).filter(  # filtra pelo admin, neste caso so vai mostrar quando tiver ativo
        mostrar=True
    )
    paginator = Paginator(contatos, 5)
    page = request.GET.get("p")
    contatos = paginator.get_page(page)

    return render(request, "contatos/index.html", {"contatos": contatos})


def ver_contato(request, contato_id):
    # contato = Contato.objects.get(id=contato_id) # mostra o conta mesmo quando tiver no modo de ver
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, "contatos/ver_contato.html", {"contato": contato})


def busca(request):
    termo = request.GET.get("termo")
    
    # if termo is None:
    #     raise Http404()
    
    if not termo:
        messages.add_message(request, messages.ERROR, 'Campo pesquisa não pode ficar vazio')
        return redirect('index')
    
    campos = Concat("nome", Value(" "), "sobrenome")

    # contatos = Contato.objects.order_by("-id").filter(  # faz uma pesquisa na base do filter
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo), mostrar=True
    # )

    contatos = Contato.objects.annotate(
        nome_completo=campos  # união de duas tabelas diferente para pesquisa unsado o nome_completo como exemplo
    ).filter(Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo), mostrar=True)

    paginator = Paginator(contatos, 5)
    page = request.GET.get("p")
    contatos = paginator.get_page(page)

    return render(request, "contatos/index.html", {"contatos": contatos})

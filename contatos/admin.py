from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = (  # mostra campo
        "id",
        "nome",
        "sobrenome",
        "telefone",
        "email",
        "data_criacao",
        "categoria",
        "mostrar",
    )

    list_display_links = (  # links para edição
        "id",
        "nome",
    )

    # list_filter = ("nome",) #filtra de pesquisa por nome

    list_per_page = 5  # paginação

    search_fields = (  # pesquisa
        "nome",
        "telefone",
    )

    list_editable = (  # habilita a edição na pagina principal do admin
        "telefone",
        "mostrar",
    )


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)

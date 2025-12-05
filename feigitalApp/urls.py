from django.urls import path
from .views import *


urlpatterns = [
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:produto_id>/', add_to_cart, name='add_to_cart'),
    path('carrinho/update/<int:item_id>/', atualizar_item, name='atualizar_item'),
    path('carrinho/remove/<int:item_id>/', remover_item, name='remover_item'),
    path('carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'),

    path('listar/', ListarProdutos.as_view(), name='lista_produtos'),
    path('adicionar/', AdicionarProduto.as_view(),name='criar_produto'),
    path('editar/<int:id>', EditarProduto.as_view(), name='editar_produto'),
    path('deletar/<int:id>', DeletarProduto.as_view, name='deletar_produto'),

    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('logout/', logout_view, name='logout'),
]
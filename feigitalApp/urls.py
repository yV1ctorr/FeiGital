from django.urls import path
from .views import *


urlpatterns = [
    path('cadastro/', CadastroUsuario.as_view(), name='cadastro_usuario'),
    # path('login/', LoginUsuario.as_view(), name='login_usuario'),

    path('listar/', ListarProduto.as_view(), name='listar_produtos'),
    path('adicionar/', AdicionarProduto.as_view(),name='criar_produto'),
    path('editar/<int:id>', EditarProduto.as_view(), name='editar_produto'),
    path('deletar/<int:id>', DeletarProduto.as_view(), name='deletar_produto'),

    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:produto_id>/', add_to_cart, name='add_to_cart'),
    path('carrinho/update/<int:item_id>/', atualizar_item, name='atualizar_item'),
    path('carrinho/remove/<int:item_id>/', remover_item, name='remover_item'),
    path('carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'),
]
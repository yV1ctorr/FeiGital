from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('cadastro/', CadastroUsuario.as_view(), name='cadastro_usuario'),
    path('login/', LoginUsuario.as_view(), name='login_usuario'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('', ListarProduto.as_view(), name='index_produtos'),
    path('listar/', ListarProduto.as_view(), name='listar_produto'),
    path('adicionar/', AdicionarProduto.as_view(),name='criar_produto'),
    path('editar/<int:pk>/', EditarProduto.as_view(), name='editar_produto'),
    path('deletar/<int:pk>/', DeletarProduto.as_view(), name='deletar_produto'),

    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:produto_id>/', add_to_cart, name='add_to_cart'),
    path('carrinho/update/<int:item_id>/', atualizar_item, name='atualizar_item'),
    path('carrinho/remove/<int:item_id>/', remover_item, name='remover_item'),
    path('carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'),
    path('checkout/', checkout, name='checkout'),
    path('pedido/sucesso/<int:pk>/', pedido_sucesso, name='pedido_sucesso'),
    path('pedido/atualizar/<int:pedido_id>/', atualizar_status_pedido, name='atualizar_status_pedido'),
    path('dashboard/', dashboard_feirante, name='dashboard_feirante'),
    path('meus-pedidos/', meus_pedidos, name='meus_pedidos'),
]
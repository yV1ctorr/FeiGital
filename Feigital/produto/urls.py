from django.urls import path
from .views import ListarProdutos, criarProduto, atualizarProduto, deletarProduto 

urlpatterns = [
    path('Listar/', ListarProdutos.as_view(), name='produtos'),
    path('Adicionar/', criarProduto.as_view(), name='Criar_Produto'),
    path('Editar/<int:pk>', atualizarProduto.as_view(), name='Atualizar_Produto'),
    path('Deletar/<int:pk>/', deletarProduto.as_view(), name='Deletar_Produto')
]
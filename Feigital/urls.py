from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

]


from django.urls import path
from feigitalApp import views


urlpatterns = [
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:produto_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrinho/update/<int:item_id>/', views.atualizar_item, name='atualizar_item'),
    path('carrinho/remove/<int:item_id>/', views.remover_item, name='remover_item'),
    path('carrinho/limpar/', views.limpar_carrinho, name='limpar_carrinho'),
]

from django.urls import path
from feigitalApp import views

urlpatterns = [
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/novo/', views.criar_produto, name='criar_produto'),
    path('produtos/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:id>/deletar/', views.deletar_produto, name='deletar_produto'),
]
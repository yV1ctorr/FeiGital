from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *

# HOME
def home(request):
    return render(request, "home.html")


# USUARIO
class CadastroUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/cadastro.html'
    success_url = reverse_lazy('login_usuario')

class LoginUsuario(LoginView):
    template_name = 'usuario/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.tipo == 'feirante':
            return reverse_lazy('cadastrar_produto')

        if user.tipo == 'cliente':
            return reverse_lazy('listar_produto')
        
        return reverse_lazy('login_usuario')

# class LogoutUsuario(LogoutView):
#     next_page = reverse_lazy('login_usuario')


#PRODUTOS
class ListarProduto(ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'produto/listar.html'

class AdicionarProduto(CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/adicionar.html'

class EditarProduto(UpdateView):
    model = Produto
    form_class = ProdutoForm
    context_object_name = 'produtos'
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/editar.html'

class DeletarProduto(DeleteView):
    model = Produto
    context_object_name = 'produtos'
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/deletar.html'


# CARRINHO
@login_required
def add_to_cart(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        produto=produto
    )

    if not created:
        item.quantidade += 1

    item.save()
    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'carrinho.html', {
        'cart': cart,
        'items': cart.items.all(),
        'total': cart.total()
    })

@login_required
def atualizar_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    quantidade = int(request.POST.get('quantidade'))
    item.quantidade = quantidade
    item.save()
    return redirect('ver_carrinho')

@login_required
def remover_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('ver_carrinho')

@login_required
def limpar_carrinho(request):
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return redirect('ver_carrinho')
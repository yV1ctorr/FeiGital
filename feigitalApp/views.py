from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Produto, Cart, CartItem, Pedido, Dashboard
from .forms import ProdutoForm, PedidoForm, CadastroForm

# AUTH
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm


# -------------------------
#  PRODUTOS (CRUD)
# -------------------------

class ListarProdutos(ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'produto/listar.html'


class AdicionarProduto(CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('listar_produtos')
    template_name = 'produto/adicionar.html'

    def form_valid(self, form):
        form.instance.banca = self.request.user  # banca = User (FK)
        return super().form_valid(form)


class EditarProduto(UpdateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('listar_produtos')
    template_name = 'produto/editar.html'


class DeletarProduto(DeleteView):
    model = Produto
    context_object_name = 'produtos'
    success_url = reverse_lazy('listar_produtos')
    template_name = 'produto/deletar.html'


# -------------------------
#  CARRINHO
# -------------------------

@login_required
def add_to_cart(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, produto=produto)
    if not created:
        item.quantidade += 1

    item.save()
    return redirect('ver_carrinho')


@login_required
def ver_carrinho(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
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


# -------------------------
#  PEDIDOS
# -------------------------

@login_required
def criar_pedido(request):
    cart = Cart.objects.get(user=request.user)

    if not cart.items.exists():
        return redirect('ver_carrinho')

    pedido = Pedido.objects.create(user=request.user, cart=cart)

    # atualizar dashboard
    for item in cart.items.all():
        feirante_user = item.produto.banca  # FK para User

        dash, created = Dashboard.objects.get_or_create(
            feirante=feirante_user,
            produto=item.produto
        )
        dash.atualizar(item.quantidade)

    # limpar carrinho
    cart.items.all().delete()

    return redirect('detalhes_pedido', pedido_id=pedido.id)


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user)
    return render(request, 'pedido/listar.html', {'pedidos': pedidos})


@login_required
def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedido/detalhes.html', {'pedido': pedido})


# -------------------------
#  DASHBOARD (FEIRANTE)
# -------------------------

@login_required
def dashboard(request):
    vendas = Dashboard.objects.filter(feirante=request.user)
    total_vendas = sum(v.total_vendido for v in vendas)

    return render(request, 'dashboard.html', {
        'vendas': vendas,
        'total_vendas': total_vendas
    })


# -------------------------
#  AUTENTICAÇÃO
# -------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('listar_produtos')

    else:
        form = AuthenticationForm()

    return render(request, 'contas/login.html', {'form': form})


def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('listar_produtos')

    else:
        form = CadastroForm()

    return render(request, 'contas/cadastro.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login')

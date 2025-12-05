from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Produto, Cart, CartItem
from .forms import ProdutoForm

# -------------------------
#  PERFIL
# -------------------------

from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

@login_required
def perfil(request):
    return render(request, 'perfil.html')

# -------------------------
#  EDITAR PERFIL
# -------------------------

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

# -------------------------
#  DASHBOARD
# -------------------------

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# -------------------------
#  PRODUTOS (CRUD)
# -------------------------

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista.html', {'produtos': produtos})


def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()

    return render(request, 'produtos/form.html', {'form': form})


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produtos/form.html', {'form': form})


def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')

    return render(request, 'produtos/confirmar_delete.html', {'produto': produto})


# -------------------------
#  CARRINHO
# -------------------------

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

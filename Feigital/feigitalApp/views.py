from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *
import qrcode
from io import BytesIO
import base64

# HOME
def home(request):
    produtos_recentes = Produto.objects.all().order_by('-id')[:4]
    return render(request, "home.html", {'produtos': produtos_recentes})


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
        return reverse_lazy('home')


#PRODUTOS
class ListarProduto(ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'produto/listar.html'

class AdicionarProduto(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/adicionar.html'

    def test_func(self):
        return self.request.user.tipo == 'feirante'

    def form_valid(self, form):
        form.instance.banca = self.request.user
        return super().form_valid(form)

class EditarProduto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    context_object_name = 'produtos'
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/editar.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.tipo == 'feirante' and obj.banca == self.request.user

class DeletarProduto(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Produto
    context_object_name = 'produtos'
    success_url = reverse_lazy('listar_produto')
    template_name = 'produto/deletar.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.tipo == 'feirante' and obj.banca == self.request.user


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
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('ver_carrinho')

    if not cart.items.exists():
        return redirect('ver_carrinho')
    
    # Create Pedido
    pedido = Pedido.objects.create(
        user=request.user,
        valor_total=cart.total()
    )
    
    # Create ItemPedido for each CartItem
    for item in cart.items.all():
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            quantidade=item.quantidade,
            preco_unitario=item.produto.preco,
            subtotal=item.subtotal()
        )
    
    # Clear Cart
    cart.items.all().delete()
    
    return redirect('pedido_sucesso', pk=pedido.pk)

@login_required
def pedido_sucesso(request, pk):
    try:
        pedido = Pedido.objects.get(pk=pk, user=request.user)
    except Pedido.DoesNotExist:
        return redirect('home')

    # Gerar QR Code
    qr_data = f"Pedido #{pedido.id} - Cliente: {pedido.user.username}"
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
        
    return render(request, 'pedido/sucesso.html', {'pedido': pedido, 'qr_code': img_str})

@login_required
def remover_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('ver_carrinho')

@login_required
def limpar_carrinho(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
    except Cart.DoesNotExist:
        pass
    return redirect('ver_carrinho')

@login_required
def dashboard_feirante(request):
    if request.user.tipo != 'feirante':
        return redirect('home')
    
    # Itens vendidos por este feirante
    itens_vendidos = ItemPedido.objects.filter(produto__banca=request.user).order_by('-pedido__data_criacao')
    
    total_vendas = sum(item.subtotal for item in itens_vendidos)
    
    return render(request, 'usuario/dashboard.html', {
        'itens_vendidos': itens_vendidos,
        'total_vendas': total_vendas,
        'status_choices': Pedido.STATUS_CHOICES
    })

@login_required
def atualizar_status_pedido(request, pedido_id):
    if request.user.tipo != 'feirante':
        return redirect('home')
    
    if request.method == 'POST':
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verifica se o feirante tem algum item em ordem
        has_item = ItemPedido.objects.filter(pedido=pedido, produto__banca=request.user).exists()
        
        if has_item:
            novo_status = request.POST.get('status')
            if novo_status:
                pedido.status = novo_status
                pedido.save()
    
    return redirect('dashboard_feirante')

@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criacao')
    return render(request, 'pedido/historico.html', {'pedidos': pedidos})

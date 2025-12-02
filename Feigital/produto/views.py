from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Produto
from .forms import ProdutoForm

class ListarProdutos(ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'produto/listar.html'

class criarProduto(CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos')
    template_name = 'produto/criar.html'

class atualizarProduto(UpdateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos')
    template_name = 'produto/atualizar.html'

class deletarProduto(DeleteView):
    model = Produto
    success_url = reverse_lazy('produtos')
    template_name = 'produto/deletar.html'


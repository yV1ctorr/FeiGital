from django import forms
from .models import Produto, Pedido, User
from django.contrib.auth.forms import UserCreationForm


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'validade', 'banca', 'img']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status']


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from django import forms
from .models import Produto
from django.contrib.auth.forms import UserCreationForm

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'validade', 'banca', 'img']
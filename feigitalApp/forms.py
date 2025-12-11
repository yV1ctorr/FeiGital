from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'validade',  'img']
 
# class UsuarioForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = Usuario
#         fields = ['username', 'email', 'tipo', 'password1', 'password2']
# models.py

from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True)
    validade = models.DateField()
    banca = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrinho de {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

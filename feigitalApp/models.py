from django.db import models
from django.contrib.auth.models import AbstractUser


# class Usuario(AbstractUser):
#     TIPO_USER = [
#         ('feirante', 'Feirante'),
#         ('cliente', 'Cliente')
#     ]
#     tipo = models.CharField(choices=TIPO_USER)

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateField()
    banca = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="produtos")
    img = models.ImageField(upload_to='/media', blank=True, null=True)

    def __str__(self):
        return self.nome

class Cart(models.Model):
    # user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
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

from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    TIPO_USER = [
        ('feirante', 'Feirante'),
        ('cliente', 'Cliente')
    ]
    tipo = models.CharField(choices=TIPO_USER)

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateField()
    banca = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="produtos")
    img = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.nome

class Cart(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
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

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('em_separacao', 'Em separação'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
    ]
    
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos")
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"
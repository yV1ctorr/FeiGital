from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

# PRODUTO
class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateField()
    banca = models.ForeignKey(User, on_delete=models.CASCADE, related_name="produtos")
    img = models.ImageField(upload_to='produto/img', blank=True, null=True)

    def __str__(self):
        return self.nome


# CARRINHO
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


# PEDIDO
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('separacao', 'Em Separação'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qrcodes', blank=True, null=True)

    # GERA QR CODE AUTOMÁTICO
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            data = f"Pedido #{self.id} - Cliente: {self.user.username}"
            img = qrcode.make(data)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"pedido_{self.id}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
            super().save(*args, **kwargs)

    def total_pedido(self):
        return self.cart.total()

    def __str__(self):
        return f"Pedido {self.id} - {self.user.username}"


# DASHBOARD
class Dashboard(models.Model):
    feirante = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_vendida = models.PositiveIntegerField(default=0)
    total_vendido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def atualizar(self, quantidade):
        self.quantidade_vendida += quantidade
        self.total_vendido += self.produto.preco * quantidade
        self.save()

    def __str__(self):
        return f"{self.feirante.username} - {self.produto.nome}"

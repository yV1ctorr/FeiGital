from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length = 50)
    preco = models.DecimalField(max_digits = 8, decimal_places = 2)
    validade = models.DateField(null = True, blank= True)
    banca = models.IntegerField()
    #foto = models.ImageField(upload_to='produto/templates/img')

    def __str__(self):
        return self.nome

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from feigitalApp.models import Produto
from datetime import date, timedelta
import random

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste (admin, feirante, cliente, produtos)'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando seed...')

        # 1. Criar Superusuário (Admin)
        if not Usuario.objects.filter(username='admin').exists():
            Usuario.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin criado (admin/admin123)'))
        else:
            self.stdout.write('Admin ja existe.')

        # 2. Criar Feirante
        if not Usuario.objects.filter(username='feirante').exists():
            Usuario.objects.create_user(username='feirante', email='feirante@example.com', password='feirante123', tipo='feirante')
            self.stdout.write(self.style.SUCCESS('Feirante criado (feirante/feirante123)'))
        else:
            self.stdout.write('Feirante ja existe.')

        # 3. Criar Cliente
        if not Usuario.objects.filter(username='cliente').exists():
            Usuario.objects.create_user(username='cliente', email='cliente@example.com', password='cliente123', tipo='cliente')
            self.stdout.write(self.style.SUCCESS('Cliente criado (cliente/cliente123)'))
        else:
            self.stdout.write('Cliente ja existe.')

        # 4. Criar Produtos para o Feirante
        feirante = Usuario.objects.get(username='feirante')
        
        produtos_data = [
            {'nome': 'Tomate', 'preco': 5.00},
            {'nome': 'Alface', 'preco': 2.50},
            {'nome': 'Cenoura', 'preco': 4.00},
            {'nome': 'Batata', 'preco': 6.00},
            {'nome': 'Banana', 'preco': 3.50},
        ]

        for p_data in produtos_data:
            if not Produto.objects.filter(nome=p_data['nome'], banca=feirante).exists():
                Produto.objects.create(
                    nome=p_data['nome'],
                    preco=p_data['preco'],
                    validade=date.today() + timedelta(days=7),
                    banca=feirante
                )
                self.stdout.write(self.style.SUCCESS(f"Produto {p_data['nome']} criado."))
            else:
                self.stdout.write(f"Produto {p_data['nome']} ja existe.")

        self.stdout.write(self.style.SUCCESS('Seed concluido com sucesso!'))

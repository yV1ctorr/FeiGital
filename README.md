# FeiGital

Sistema de e-commerce para feiras digitais desenvolvido em Django. Conecta feirantes e clientes, permitindo pedidos online de produtos frescos e retirada na banca.

## Funcionalidades
- Feirante: painel de vendas, cadastro e gerenciamento de produtos.
- Cliente: pedidos, histórico e QR Code para retirada.
- Carrinho de compras e checkout.
- Interface responsiva.

## Pré-requisitos
- Python 3.10+

## Instalação e Execução
1. Ambiente virtual (recomendado)
   - Windows:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
2. Dependências
   ```bash
   pip install -r requirements.txt
   ```
3. Banco de dados
   ```bash
   python manage.py migrate
   ```
4. Dados de teste (opcional)
   ```bash
   python manage.py seed_demo
   ```
5. Servidor
   ```bash
   python manage.py runserver
   ```
6. Acesso
   http://127.0.0.1:8000/

## Credenciais de Teste
- Feirante: usuário `feirante`, senha `feirante123`
- Cliente: usuário `cliente`, senha `cliente123`
- Admin: usuário `admin`, senha `admin123`

## Estrutura do Projeto
- `feigitalApp/`: models, views, urls, forms.
- `templates/`: HTML.
- `static/`: CSS e imagens do sistema.
- `media/`: uploads dos usuários.

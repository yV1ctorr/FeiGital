from django.contrib import admin
from .models import Usuario, Produto, Cart, CartItem, Pedido, ItemPedido

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo', 'is_active')
    list_filter = ('tipo', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'banca', 'validade')
    list_filter = ('banca',)
    search_fields = ('nome',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'valor_total', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('user__username', 'id')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'subtotal')
    list_filter = ('pedido__status',)

admin.site.register(Cart)
admin.site.register(CartItem)

# Customização do Painel Admin
admin.site.site_header = 'Administração FeiGital'
admin.site.site_title = 'FeiGital Admin'
admin.site.index_title = 'Painel de Controle'

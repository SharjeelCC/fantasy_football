from django.contrib import admin
from .models import Player, Transaction

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'value', 'for_sale', 'sale_price', 'owner_team')
    search_fields = ('name', 'position')
    list_filter = ('position', 'for_sale')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('player', 'buyer', 'seller', 'transfer_amount', 'transfer_date')
    search_fields = ('player__name', 'buyer__username', 'seller__username')
    list_filter = ('transfer_date',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Transaction, TransactionAdmin)
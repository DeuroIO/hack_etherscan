from django.contrib import admin

from .models import *


class TokenAdmin(admin.ModelAdmin):
    list_display = ('coin_name','contract_address','status')
    search_fields = ['coin_name','contract_address',]


class AccountAdmin(admin.ModelAdmin):
    list_display = ('gussed_name','account_address')
    search_fields = ['gussed_name','account_address', ]

class TokenTransactionAdmin(admin.ModelAdmin):
    list_display = ('token_name','tx_hash','timestamp','from_account','to_account','quantity')
    search_fields = ['token_name__coin_name',]

class EtherDeltaTokenTradeAdmin(admin.ModelAdmin):
    list_display = ('token_name','tx_hash','timestamp','price','is_buy','amount','amount_base','buyer','seller')
    search_fields = ['token_name__coin_name',]

admin.site.register(Token,TokenAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(TokenTransaction,TokenTransactionAdmin)
admin.site.register(TopTokenHolder)
admin.site.register(TopTokenTransaction)
admin.site.register(EtherDeltaTokenTrade,EtherDeltaTokenTradeAdmin)
admin.site.register(EtherTransactionHash)

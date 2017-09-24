from django.contrib import admin
from .models import *
# Register your models here.
class EtherDeltaDailyStatAdmin(admin.ModelAdmin):
    list_display = ('token_name','timestamp','total_eth_buy','total_eth_sell','avg_price')
    search_fields = ['token_name__coin_name',]

admin.site.register(EtherDeltaDailyStat,EtherDeltaDailyStatAdmin)
admin.site.register(TopEtherDeltaTransaction)
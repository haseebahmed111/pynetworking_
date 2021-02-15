from django.contrib import admin
from .models import PendingTransaction,Exchanger
# Register your models here.

class PendingTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'send_to', 'pending', 'date')

class ExchangerAdmin(admin.ModelAdmin):
    list_display = ('user', 'borrowed_amount', 'join_date')


admin.site.register(PendingTransaction,PendingTransactionAdmin)
admin.site.register(Exchanger,ExchangerAdmin)

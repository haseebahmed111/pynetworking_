from django.contrib import admin
from .models import Member, Account, MembershipType, Membership, Referral,Transaction,ContactUs
# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'cnic', 'phone_number', 'gender', 'membership','account','referral' )
    search_fields = ('user__username','cnic','phone_number')
    list_filter = ('membership__end_date',)


class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'months', 'max_levels', 'max_referrals', 'commission_percentage')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_commission', 'is_approved')
    search_fields = ('user__username',)


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_referrals', 'referred_by','commission')


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'start_date', 'end_date')
    ordering = ('end_date',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','amount','send_to', 'date')


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','subject','phone_number')


admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipType, MembershipTypeAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(ContactUs,ContactUsAdmin)

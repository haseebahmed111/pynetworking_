from django.contrib import admin
from .models import Rewards,RewardClaimRecord
# Register your models here.


class RewardAdmin(admin.ModelAdmin):
    list_display = ('title','bonus','membership')


class RewardRecordAdmin(admin.ModelAdmin):
    list_display = ('user','reward','date_time')


admin.site.register(Rewards, RewardAdmin)
admin.site.register(RewardClaimRecord, RewardRecordAdmin)
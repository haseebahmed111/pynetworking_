from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Exchanger(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    borrowed_amount = models.FloatField(default=0)
    join_date = models.DateTimeField(default=timezone.now)


class PendingTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Exchanger_Sender')
    amount = models.FloatField(default=0)
    send_to = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='Member_Receiver')
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    pending = models.BooleanField(default=True)


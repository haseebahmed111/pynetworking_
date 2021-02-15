from django.db import models
from member.models import MembershipType
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Rewards(models.Model):
    title = models.CharField(max_length=256)
    conditions = models.TextField(max_length=10240)
    bonus = models.FloatField()
    membership = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class RewardClaimRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Rewards, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)

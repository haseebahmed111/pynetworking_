from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    balance = models.FloatField(default=0)
    total_commission = models.FloatField(default=0)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return str('A# '+ str(self.pk) +' B: '+ str(self.balance))


class MembershipType(models.Model):
    title = models.CharField(max_length=256)
    price = models.IntegerField(default=0)
    max_levels = models.IntegerField(default=0)
    max_referrals = models.IntegerField(default=7)
    months = models.IntegerField(default=0)
    commission_percentage = models.IntegerField(default=5)
    description = models.TextField(max_length=1024, blank=True)

    def __str__(self):
        return str (str(self.pk)+ '. ' + self.title)


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    type = models.ForeignKey(MembershipType,default='free', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.user.username +' : ' +self.type.title)


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='User', primary_key=True)
    referred_by = models.ForeignKey(User,default='admin',related_name='referral', on_delete=models.CASCADE)
    total_referrals = models.IntegerField(default=0)
    commission = models.FloatField(default=0)
    # commission given to referred_by user
    def __str__(self):
        return str(self.user.username + ' <- '+self.referred_by.username)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # picture = models.ImageField(upload_to='member/profile_pictures/', default='logo.png', blank=True)
    cnic = models.CharField(max_length=13, help_text="Without dashes")
    birth_date = models.DateField()
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES,blank=True)
    phone_number = models.CharField(max_length=11,help_text="Starting with 03XX")
    address = models.TextField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=256, blank=True)
    # cnic_pic_front = models.ImageField(upload_to='member/cnic/', blank=True)
    # cnic_pic_rear = models.ImageField(upload_to='member/cnic/', blank=True)
    phone_number_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    account = models.OneToOneField(Account,on_delete=models.CASCADE)
    membership = models.OneToOneField(Membership,on_delete=models.CASCADE)
    referral = models.OneToOneField(Referral,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Sender')
    amount = models.FloatField(default=0)
    send_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Receiver')
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)
    message = models.TextField(max_length=1024)


# class Site(models.Model):
#    total_users = models.IntegerField(default=0)
#    free_users = models.IntegerField(default=0)
#    basic_users = models.IntegerField(default=0)
#    premium_users = models.IntegerField(default=0)
#    ultimate_users = models.IntegerField(default=0)




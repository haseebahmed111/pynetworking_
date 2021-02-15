from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member, Transaction, ContactUs

YEARS = [x for x in range(1940, 2020)]

GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class MemberForm(forms.ModelForm):
    referral_username = forms.CharField(max_length=150, help_text="Enter Username of Referral eg. User1234 ",required=False)
    birth_date= forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Member
        fields = ('phone_number','cnic','gender',)


class MemberFormReferral(forms.ModelForm):
    birth_date= forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Member
        fields = ('phone_number','cnic','gender',)



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class MemberEditForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('cnic', 'phone_number', 'gender', 'address', 'city', 'state', 'country')


class TransactionForm(forms.ModelForm):
    send_to = forms.CharField(max_length=150,label='Send to')
    birth_date = forms.DateField(label='Enter Birth Date for verification', widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Transaction
        fields = ('amount',)


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name','phone_number','subject', 'message')


class PasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Member
        fields = ()

from django import forms
from .models import PendingTransaction

YEARS = [x for x in range(1940, 2020)]

class PendingTransactionForm(forms.ModelForm):
    send_to = forms.CharField(max_length=150,label='Send to')
    birth_date = forms.DateField(label='Enter Birth Date for verification', widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = PendingTransaction
        fields = ('amount','pending')
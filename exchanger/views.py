from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PendingTransactionForm
from django.contrib.auth.models import Group
from member.models import Member, Transaction
from .models import PendingTransaction, Exchanger
from member.forms import PasswordForm
from django.contrib.auth.hashers import check_password

# Create your views here.

@login_required
def send_balance_exchanger(request):
    group = Group.objects.get(name='Exchanger')
    if group in request.user.groups.all():
        successful = False
        error = False
        error_message = 'no'
        if request.method == 'POST':
            form = PendingTransactionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('amount')
                send_to = form.cleaned_data.get('send_to')
                birth_date = form.cleaned_data.get('birth_date')
                pending = form.cleaned_data.get('pending')
                if amount > 0:
                    if amount <= 100:
                        member = Member.objects.get(user=request.user)
                        if amount <= member.account.balance:
                            try:
                                send_to_member = Member.objects.get(user__username__exact=send_to)
                                if birth_date == member.birth_date:
                                    member.account.balance = member.account.balance - amount
                                    member.account.save()
                                    if pending:
                                        trans = form.save(commit=False)
                                        trans.user = request.user
                                        trans.send_to = send_to_member.user
                                        trans.save()
                                        error=True
                                        error_message = "Amount deducted but Transaction operation state is pending!"

                                    else:
                                        send_to_member.account.balance = send_to_member.account.balance + amount
                                        send_to_member.account.save()
                                        trans = Transaction.objects.create(amount=amount,send_to=send_to_member.user,user=request.user)
                                        trans.save()
                                        successful = True
                                else:
                                    error = True
                                    error_message = 'Verification failed. Enter correct birth date!'
                            except Member.DoesNotExist:
                                error = True
                                error_message = 'Username you entered is invalid!'


                        else:
                            error = True
                            error_message = 'Your account balance is not enough'
                    else:
                        error = True
                        error_message = 'Enter amount less or equal to 100'

                else:
                    error = True
                    error_message = 'Invalid amount'
        else:
            form = PendingTransactionForm()
        return render(request, 'exchanger/send_balance.html', {'form':form, 'error':error, 'error_message':error_message, 'confirm':successful})
    message = "Sorry! You are not part of Exchanger Team."
    return render(request, 'error_page.html', {'message': message})


@login_required
def pending_list(request):
    group = Group.objects.get(name='Exchanger')
    if group in request.user.groups.all():
        pending = PendingTransaction.objects.filter(user=request.user)
        return render(request, 'exchanger/pending_transaction.html', {'send': pending})
    message = "Sorry! You are not part of Exchanger Team."
    return render(request, 'error_page.html', {'message': message})


@login_required
def send_pending(request,pk):
    trans = PendingTransaction.objects.get(pk=pk)
    error_message = ''
    error = False
    group = Group.objects.get(name='Exchanger')
    if group in request.user.groups.all():

        try:
            member_send_to = Member.objects.get(user=trans.send_to)
        except Member.DoesNotExist:
            member_send_to = Member.objects.get(user=request.user)
            error = True
            error_message = "User no longer exists."
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                if trans.user == request.user:
                    password1 = form.cleaned_data.get('password')
                    password = trans.user.password
                    if check_password(password1, password):
                        member_send_to.account.balance = member_send_to.account.balance + trans.amount
                        member_send_to.account.save()
                        send_trans = Transaction.objects.create(user=trans.user,send_to=trans.send_to,amount=trans.amount)
                        send_trans.save()
                        trans.delete()
                        return redirect('transaction_history')
                    else:
                        error = True
                        error_message = 'Wrong Password'
                else:
                    error = True
                    error_message = 'You are not allowed to make this Operation'
            else:
                print(form.errors)
        else:
            form = PasswordForm()
        return render(request, 'exchanger/pending_confirmation.html', {'form':form, 'trans': trans,
                                                                       'error_message': error_message, 'error': error})

    message = "Sorry! You are not part of Exchanger Team."
    return render(request, 'error_page.html', {'message': message})

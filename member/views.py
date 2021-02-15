from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from .forms import UserEditForm, UserForm, MemberForm, MemberEditForm, TransactionForm,MemberFormReferral,ContactUsForm, PasswordForm
from .models import Member, Membership, Account, Referral, MembershipType, Transaction
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.contrib.auth.hashers import check_password
from exchanger.models import PendingTransaction as PendingAmount
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

# Create your views here.


def index(request):
    return render(request,'member/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in!")


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        member_form = MemberForm(data=request.POST)
        if user_form.is_valid() and member_form.is_valid():
            referral = member_form.cleaned_data.get('referral_username')
            date_of_birth = member_form.cleaned_data.get('birth_date')
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.birth_date = date_of_birth
            admin_username = 'admin'

            try:
                refer_by_member = Member.objects.get(user__username__exact=referral)
                if refer_by_member.referral.total_referrals >= refer_by_member.membership.type.max_referrals:
                    refer_by_member = Member.objects.get(user__username__exact=admin_username)

            except Member.DoesNotExist:
                refer_by_member = Member.objects.get(user__username__exact=admin_username)

            refer_by_member.referral.total_referrals = refer_by_member.referral.total_referrals + 1
            refer_by_member.referral.save()
            member.referral = Referral.objects.create(user=user,referred_by=refer_by_member.user)
            member.referral.save()

            member.account = Account.objects.create(user=user)
            member.account.save()

            member.membership = Membership.objects.create(user=user, type=MembershipType.objects.get(title__contains='Free'))
            member.membership.start_date = timezone.datetime.now()
            member.membership.end_date = (member.membership.start_date + relativedelta(months=member.membership.type.months))
            member.membership.save()
            member.save()
            template = get_template('mail/email.html')
            content = template.render({'user': user})

            msg = EmailMultiAlternatives(subject='Welcome - Py Networking', body=content,
                                         from_email='info.pynetworking@gmail.com', to=[user.email, ])
            msg.attach_alternative(content, "text/html")
            msg.send()
            login(request, user)
            return redirect('dashboard')
        else:
            print(user_form.errors, member_form.errors)
    else:
        user_form = UserForm()
        member_form = MemberForm()
    return render(request, 'member/signup.html', {'user_form': user_form, 'member_form': member_form})


def register_by_referral(request,username):
    if request.user.is_authenticated:
        return redirect('dashboard')
    admin_username = 'admin'
    try:
        refer_by_member = Member.objects.get(user__username__exact=username)
        if refer_by_member.referral.total_referrals >= refer_by_member.membership.type.max_referrals:
            refer_by_member = Member.objects.get(user__username__exact=admin_username)

    except Member.DoesNotExist:
        refer_by_member = Member.objects.get(user__username__exact=admin_username)
        username=admin_username

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        member_form = MemberFormReferral(data=request.POST)
        if user_form.is_valid() and member_form.is_valid():
            date_of_birth = member_form.cleaned_data.get('birth_date')

            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.birth_date = date_of_birth

            refer_by_member.referral.total_referrals = refer_by_member.referral.total_referrals + 1
            refer_by_member.referral.save()
            member.referral = Referral.objects.create(user=user,referred_by=refer_by_member.user)
            member.referral.save()

            member.account = Account.objects.create(user=user)
            member.account.save()

            member.membership = Membership.objects.create(user=user, type=MembershipType.objects.get(title__contains='Free'))
            member.membership.start_date = timezone.datetime.now()
            member.membership.end_date = (member.membership.start_date + relativedelta(months=member.membership.type.months))
            member.membership.save()
            member.save()
            template = get_template('mail/email.html')
            content = template.render({'user': user})

            msg = EmailMultiAlternatives(subject='Welcome - Py Networking', body=content,
                                         from_email='info.pynetworking@gmail.com', to=[user.email, ])
            msg.attach_alternative(content, "text/html")
            msg.send()
            login(request, user)
            return redirect('dashboard')
        else:
            print(user_form.errors, member_form.errors)
    else:
        user_form = UserForm()
        member_form = MemberFormReferral()
    return render(request, 'member/signup_referral.html', {'user_form': user_form, 'member_form': member_form,'username':username})


@login_required
def dashboard(request):
    member = Member.objects.get(user=request.user)
    membership = member.membership
    account = member.account
    balance = account.balance
    total_commission = account.total_commission
    try:
        pending_amounts = PendingAmount.objects.filter(send_to=request.user)
        pending_amount = 0.0
        is_pending = True
        if pending_amounts.count() > 1:
            for pending in pending_amounts:
                pending_amount = pending_amount + pending.amount
        else:
            pending_amount = pending_amounts.get(send_to=request.user).amount
    except PendingAmount.DoesNotExist:
        pending_amount = 0.0
        is_pending = False

    total_referral = member.referral.total_referrals
    referral_used = total_referral / membership.type.max_referrals
    referral_used = referral_used * 100
    referral_used = Decimal(referral_used)
    referral_used = round(referral_used, 2)

    if referral_used > 79:
        referral_bar_color = 'success'
    elif referral_used > 59:
        referral_bar_color = 'info'
    elif referral_used > 39:
        referral_bar_color = 'primary'
    elif referral_used > 19:
        referral_bar_color = 'warning'
    else:
        referral_bar_color = 'danger'

    if membership.type.title == 'Basic':
        unlocked_membership_color = 'warning'
        unlocked_membership_percent = 50

    elif membership.type.title == 'Premium':
        unlocked_membership_color = 'info'
        unlocked_membership_percent = 75

    elif membership.type.title == 'Ultimate':
        unlocked_membership_color = 'success'
        unlocked_membership_percent = 100
    else:
        unlocked_membership_color = 'danger'
        unlocked_membership_percent = 25

    return render(request,'member/dashboard.html', {'user': request.user, 'balance': balance, 'commission': total_commission,
                                                    'used_referrals': referral_used, 'referrals': total_referral,
                                                    'membership': membership,'umc':unlocked_membership_color, 'ump':unlocked_membership_percent,
                                                    'is_pending':is_pending, 'pending_amount': pending_amount,'rbc':referral_bar_color})

@login_required
def referrals(request):
    member =Member.objects.get(user=request.user)
    below = Member.objects.filter(referral__referred_by=request.user)
    return render(request,'member/referral_info.html',{'referrals':below,'member':member})


def membership_page(request):
    free = MembershipType.objects.get(title='Free')
    basic = MembershipType.objects.get(title='Basic')
    premium = MembershipType.objects.get(title='Premium')
    ultimate = MembershipType.objects.get(title='Ultimate')
    return render(request,'member/membership.html',{'free':free,'basic':basic,'premium':premium,'ultimate':ultimate})


@login_required
def buy_membership(request, mid):
    error=False
    error_message = ''
    buymembership = MembershipType.objects.get(pk=mid)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password')
            password = request.user.password
            if check_password(password1, password):
                user = request.user
                member = Member.objects.get(user=user)
                current_membership = member.membership
                account = member.account
                price = buymembership.price
                percentage = 100
                if (account.balance >= price) and (price != 0):
                    current_membership.type = buymembership
                    account.balance = account.balance - price
                    account.save()
                    current_membership.start_date = timezone.datetime.now()
                    current_membership.end_date = (current_membership.start_date + relativedelta(months=current_membership.type.months))
                    current_membership.save()
                    admin_username = 'admin'
                    admin_user = User.objects.get(username=admin_username)
                    admin_member = Member.objects.get(user=admin_user)
                    # Direct Referral
                    try:
                        # Direct 1
                        direct1 = member.referral.referred_by
                        direct1_member = Member.objects.get(user=direct1)
                        direct1_member.account.balance = direct1_member.account.balance + (price * (direct1_member.membership.type.commission_percentage/100))
                        direct1_member.account.total_commission = direct1_member.account.total_commission + (price * (direct1_member.membership.type.commission_percentage/100))
                        member.referral.commission = member.referral.commission + (price * (direct1_member.membership.type.commission_percentage/100))
                        member.referral.save()
                        direct1_member.account.save()
                        percentage = percentage - direct1.membership.type.commission_percentage

                        # Indirect 1
                        indirect1 = direct1_member.referral.referred_by
                        indirect1_member = Member.objects.get(user=indirect1)
                        if indirect1_member.membership.type.max_levels > 1:
                            indirect1_member.account.balance = indirect1_member.account.balance + (price * (5 / 100))
                            indirect1_member.account.total_commission = indirect1_member.account.total_commission + ( price * (5 / 100))
                            direct1_member.referral.commission = direct1_member.referral.commission + (price * (5 / 100))
                            direct1_member.referral.save()
                            indirect1_member.account.save()
                            percentage = percentage - 5

                        # Indirect 2
                        indirect2 = indirect1_member.referral.referred_by
                        indirect2_member = Member.objects.get(user=indirect2)
                        if indirect2_member.membership.type.max_levels > 2:
                            indirect2_member.account.balance = indirect2_member.account.balance + (price * (5 / 100))
                            indirect2_member.account.total_commission = indirect2_member.account.total_commission + (
                                    price * (5 / 100))
                            indirect1_member.referral.commission = indirect1_member.referral.commission + (price * (5 / 100))
                            indirect1_member.referral.save()
                            indirect2_member.account.save()
                            percentage = percentage - 5

                        # Indirect 3
                        indirect3 = indirect2_member.referral.referred_by
                        indirect3_member = Member.objects.get(user=indirect3)
                        if indirect3_member.membership.type.max_levels > 3:
                            indirect3_member.account.balance = indirect3_member.account.balance + (price * (5 / 100))
                            indirect3_member.account.total_commission = indirect3_member.account.total_commission + (
                                    price * (5 / 100))
                            indirect2_member.referral.commission = indirect2_member.referral.commission + (price * (5 / 100))
                            indirect2_member.referral.save()
                            indirect3_member.account.save()
                            percentage = percentage - 5

                        # Indirect 4
                        indirect4 = indirect1_member.referral.referred_by
                        indirect4_member = Member.objects.get(user=indirect4)
                        if indirect4_member.membership.type.max_levels > 4:
                            indirect4_member.account.balance = indirect4_member.account.balance + (price * (5 / 100))
                            indirect4_member.account.total_commission = indirect4_member.account.total_commission + (
                                    price * (5 / 100))
                            indirect3_member.referral.commission = indirect3_member.referral.commission + (price * (5 / 100))
                            indirect3_member.referral.save()
                            indirect4_member.account.save()
                            percentage = percentage - 5

                    except User.DoesNotExist:
                        admin_member.account.balance = admin_member.account.balance + (price*(percentage/100))
                        admin_member.account.total_commission = admin_member.account.total_commission + (price*(percentage/100))
                        admin_member.account.save()
                        percentage = percentage - percentage

                    admin_member.account.balance = admin_member.account.balance + (price * (percentage / 100))
                    admin_member.account.total_commission = admin_member.account.total_commission + (price * (percentage / 100))
                    admin_member.account.save()
                    percentage = percentage - percentage

                else:
                    no_balance = True
                    free = MembershipType.objects.get(title='Free')
                    basic = MembershipType.objects.get(title='Basic')
                    premium = MembershipType.objects.get(title='Premium')
                    ultimate = MembershipType.objects.get(title='Ultimate')
                    return render(request, 'member/membership.html',
                                  {'free': free, 'basic': basic, 'premium': premium, 'ultimate': ultimate,'no_balance':no_balance})
                return redirect('dashboard')
            else:
                error = True
                error_message = 'Wrong Password'
        else:
            print(form.errors)
    else:
        form = PasswordForm()
    return render(request, 'member/membership_purchase.html',
                  {'form': form, 'membership': buymembership, 'error_message': error_message, 'error': error})





@login_required
def edit_user(request):
    instance = Member.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        member_form = MemberEditForm(request.POST,instance=instance)
        if user_form.is_valid() and member_form.is_valid():
            user_form.save()
            member_form.save()
            return redirect('dashboard')

        else:
            print(user_form.errors,member_form.errors)
            return render(request, 'member/profile_edit.html', {'member_form': member_form, 'user_form': user_form})

    else:
        member_form = MemberEditForm(instance=instance)
        user_form = UserEditForm(instance=request.user)
    return render(request,'member/profile_edit.html',{'member_form':member_form,'user_form':user_form})


@login_required
def send_balance(request):
    successful = False
    error = False
    error_message = 'no'
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            amount = round(amount,2)
            send_to = form.cleaned_data.get('send_to')
            birth_date = form.cleaned_data.get('birth_date')
            if amount > 0:
                if amount <= 100:
                    member = Member.objects.get(user=request.user)
                    if amount <= member.account.balance:
                        try:
                            send_to_member = Member.objects.get(user__username__exact=send_to)
                            if birth_date == member.birth_date:
                                member.account.balance = member.account.balance - amount
                                member.account.save()
                                send_to_member.account.balance = send_to_member.account.balance + amount
                                send_to_member.account.save()
                                trans = form.save(commit=False)
                                trans.user = request.user
                                trans.send_to = send_to_member.user
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
        form = TransactionForm()
    return render(request,'member/send_balance.html',{'form':form,'error':error,'error_message':error_message,'confirm':successful})


@login_required
def referral_remove(request,pk):
    admin_username = 'admin'
    admin_member = Member.objects.get(user__username__exact=admin_username)
    member_remove = Member.objects.get(user_id=pk)
    member = Member.objects.get(user=request.user)
    error_message = ''
    error=False
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password')
            password = request.user.password
            if check_password(password1,password):
                try:
                    member_remove.referral.referred_by = admin_member.user
                    member_remove.referral.save()

                    member.referral.total_referrals = member.referral.total_referrals - 1
                    member.referral.save()

                    admin_member.referral.total_referrals = admin_member.referral.total_referrals + 1
                    admin_member.referral.save()
                except Member.DoesNotExist:
                    print('Member Does not exist')
                return redirect('referrals_info')
            else:
                error=True
                error_message = 'Wrong Password'
        else:
            print(form.errors)
    else:
        form = PasswordForm()
    return render(request, 'member/referral_remove.html', {'form':form, 'member':member, 'error_message':error_message, 'error':error})


def contact_us(request):
    submitted = False
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.name = request.user.username
            message.save()
            submitted = True
    else:
        form = ContactUsForm()
    return render(request,'member/contact_us.html',{'form':form,'submitted':submitted})


@login_required
def transaction_history(request):
    sent = Transaction.objects.filter(user=request.user).order_by('-date')
    received = Transaction.objects.filter(send_to=request.user).order_by('-date')

    return render(request,'member/transaction_history.html',{'sent':sent,'received':received})

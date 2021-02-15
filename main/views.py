from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import login_required
from member.models import Member, MembershipType
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Rewards,RewardClaimRecord
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def mail_test(request):
    template = get_template('mail/email.html')
    content = template.render({'user': request.user})

    msg = EmailMultiAlternatives(subject='Welcome - Py Networking', body=content,
                                 from_email='info.pynetworking@gmail.com', to = ['haseeb.ahmed1111@gmail.com', ])
    msg.attach_alternative(content,"text/html")
    msg.send()
    return render(request,'home/index.html')


def mail_template(request):
    return render(request,'mail/email.html',{'user':request.user})


@login_required
def promo_1(request,pk):
    reward = Rewards.objects.get(pk=pk)
    satisfy_promo = False
    message = ''
    error = False
    member = Member.objects.get(user=request.user)
    end_time = member.user.date_joined + relativedelta(days=30)
    if timezone.now() < end_time:
        if RewardClaimRecord.objects.filter(user=request.user, reward=reward).exists():
            error = True
            message = "Already Claimed!"
        else:
            try:
                premium_referrals = 0
                basic_referrals = 0
                ultimate_referrals = 0
                referrals = Member.objects.filter(referral__referred_by=request.user)
                count = referrals.count()
                if count > 1:
                    for referral in referrals:
                        if referral.membership.type.title == 'Basic':
                            basic_referrals = basic_referrals + 1
                        if referral.membership.type.title == 'Premium':
                            premium_referrals = premium_referrals + 1
                        if referral.membership.type.title == 'Ultimate':
                            ultimate_referrals = ultimate_referrals + 1

                    if basic_referrals >9:
                        satisfy_promo =True
                    if premium_referrals >2:
                        satisfy_promo = True
                    if ultimate_referrals > 0:
                        satisfy_promo = True
                if count == 0:
                    error = True
                    message = "You don't have any referral."

                else:
                        if referrals[0].membership.type.title == 'Ultimate':
                            satisfy_promo = True

                if satisfy_promo:
                    membership = MembershipType.objects.get(title='Premium')
                    member.membership.type = membership
                    member.membership.save()
                    member.account.balance = member.account.balance + 5
                    member.account.save()
                    error = False
                    new_record = RewardClaimRecord.objects.create(user=request.user,reward=reward)
                    new_record.save()
                    message = "You have successfully received Premium Membership and bonus of 5 py."
                else:
                    error = True
                    message = "Your task is not completed yet. Refer more people to claim your prize."

            except Member.DoesNotExist:
                error = True
                message = "You don't have any referral."
    else:
        error = True
        message = "Your account is older than 30 days."

    return render(request,'promo/promo.html',{'error':error,'message':message,'is_successful':satisfy_promo,
                                              'startup_reward':reward})


def promo_list(request):
    startup_reward = Rewards.objects.get(title='Startup')
    error = False
    message = ''
    satisfy_promo = False
    return render(request,'promo/promo.html',{'error':error,'message':message,'is_successful':satisfy_promo,
                                              'startup_reward':startup_reward})

def marketing_plan(request):
    return render(request,'marketing_plan.html')




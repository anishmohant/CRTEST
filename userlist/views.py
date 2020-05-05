from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import IntegrityError

from .models import UserList
from django.db.models import Max
from django.core.mail import send_mail

import uuid


def index(request):
    try:
        ref_code = request.GET['ref']
    except:
        ref_code = ''
    print(ref_code)
    print(request.META['SERVER_PORT'])
    context = {'code': ref_code}
    return render(request, 'index.html', context)

def initiate_email(recipient,port=None,ref_code=None):
    if port is None and ref_code is None:
        context = {
            'link': 'https://store.ui.com/collections/early-access',
            'message': 'Youre are granted an early access',
            'wish': 'Congratulations'
        }
    else:
        shareable_link = 'http://127.0.0.1:'+str(port)+'/?ref=' + ref_code + ''
        print(shareable_link)
        context = {
            'link': shareable_link,
            'message':'Please do share this link with your friends to increase your chance for an early access',
            'wish':"Thank You"
        }
    msg_html = render_to_string('message_body.html', context)
    try:
        send_mail(
            'CRTEST',
            'msg_plain',
            'no-reply@crtest.io',
            [recipient],
            html_message=msg_html,
        )
        return True
    except:
        return False


def enlist(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        referer_code = request.POST.get('code', None)
        print("dsd")
        print(referer_code)
        print(type(referer_code))
        total_entries = UserList.objects.all().count()
        own_code = str(uuid.uuid1())
        success_context = {
            'wish': 'Welcome',
            'message': 'Thanks for Signing Up, Check your mailbox for shareable link'
        }
        duplicate_context = {
            'messages': ['Email already used',
                         'Use another mail id']
        }
        if total_entries > 0:
            if referer_code =='':
                max = UserList.objects.aggregate(Max('position'))
                last_position = int(max['position__max'])
                user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code,
                                      position=last_position + 1)
                try:
                    user_entry.save()
                    initiate_email(email, int(request.META['SERVER_PORT']), own_code)
                    return render(request, 'message_body.html', success_context)
                except IntegrityError as ie:
                    print(ie)
                    return render(request, 'index.html', duplicate_context)
            else:
                referer = UserList.objects.filter(own_code=referer_code)
                referer_position = referer[0].position
                print(referer)
                if referer_position == 2:
                    referer = UserList.objects.filter(own_code=referer_code)
                    referer_email = referer[0].email
                    initiate_email(referer_email)
                UserList.objects.filter(own_code=referer_code).update(position=referer_position - 1)
                max = UserList.objects.aggregate(Max('position'))
                last_position = int(max['position__max'])
                user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=last_position+1)
                try:
                    user_entry.save()
                    initiate_email(email, int(request.META['SERVER_PORT']), own_code)
                    return render(request, 'message_body.html', success_context)
                except IntegrityError as ie:
                    print('XAXA')
                    print(ie)
                    return render(request, 'index.html', duplicate_context)


        else:
            user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=99)
            try:
                user_entry.save()
                initiate_email(email, int(request.META['SERVER_PORT']), own_code)
                return render(request, 'message_body.html', success_context)
            except IntegrityError as ie:
                print(ie)
                return render(request, 'index.html', duplicate_context)


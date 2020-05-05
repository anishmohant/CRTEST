from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

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
            'link': 'shareable_link',
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
    msg_html = render_to_string('email_message.html', context)
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
        total_entries = UserList.objects.all().count()
        own_code = str(uuid.uuid1())
        if total_entries > 0:
            referer = UserList.objects.filter(own_code=referer_code)
            referer_position = referer[0].position
            print(referer)
            if referer_position == 2:
                print("This guy is going places")
                referer = UserList.objects.filter(own_code=referer_code)
                email = referer[0].email
                print(email)
                initiate_email(email)
            UserList.objects.filter(own_code=referer_code).update(position=referer_position - 1)
            max = UserList.objects.aggregate(Max('position'))
            last_position = int(max['position__max'])
            user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=last_position+1)
            user_entry.save()
            initiate_email(email, int(request.META['SERVER_PORT']), own_code)

        else:
            user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=5)
            user_entry.save()
            initiate_email( email,int(request.META['SERVER_PORT']), own_code)

        return render(request, 'index.html', {})
# UserList.objects.get(own_code='0b9545ac-8dee-11ea-8f01-8cdcd449aef0')
# UserList.objects.get(name='baba')
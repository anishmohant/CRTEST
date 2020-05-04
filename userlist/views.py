from django.shortcuts import render
from django.http import HttpResponse
from .models import UserList
from django.db.models import Max

import uuid


def index(request):
    try:
        ref_code = request.GET['ref']
    except:
        ref_code = ''
    print(ref_code)
    context = {'code': ref_code}
    return render(request, 'index.html', context)

def enlist(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        referer_code = request.POST.get('code', None)
        print("dsd")
        print(referer_code)
        total_entries=UserList.objects.all().count()




        own_code = str(uuid.uuid1())
        if total_entries > 0:
            referer = UserList.objects.filter(own_code=referer_code)
            referer_position = referer[0].position
            print(referer)
            UserList.objects.filter(own_code=referer_code).update(position=referer_position - 1)
            max = UserList.objects.aggregate(Max('position'))
            last_position = int(max['position__max'])
            user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=last_position+1)
            user_entry.save()
        else:
            user_entry = UserList(name=name, email=email, refer_code=referer_code, own_code=own_code, position=5)
            user_entry.save()
        return render(request, 'index.html', {})
# UserList.objects.get(own_code='0b9545ac-8dee-11ea-8f01-8cdcd449aef0')
# UserList.objects.get(name='baba')
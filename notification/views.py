from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import json

from .models import Notification
# Create your views here.


def user_notification(request):
    notif_dict = {}
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(user=request.user, read=False)
        if notifs.count() == 0:
            notif_dict[0] = {'message': 'All read :)', 'level': 2, 'read': False,}
        else:
            for notif in notifs:
                notif_dict[notif.pk] = (notif.to_dict())
    else:
        notif_dict[0] = {'message': 'Please Login. :)', 'level': 2, 'read': False,}
    return JsonResponse(notif_dict)


@login_required
def notification_list(request):
    notif_list = Notification.objects.filter(user=request.user)
    for notif in notif_list:
        notif.mark_as_read
    return render(request, 'notification_list.html', {'notif_list': notif_list, })

import uuid
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from common.models import *
from common.tasks import compress


def index(request):
    c = Screenshot.objects.count()
    c = 'Total screenshots: %d' % c
    return HttpResponse(c)


@csrf_exempt
def screenshot(request):
    t = uuid.UUID(request.GET['token'])
    try:
        u = User.objects.get(token=t)
    except User.DoesNotExist:
        return HttpResponse(status=401)

    s = Screenshot.objects.create(user=u)

    f = request.FILES['file']
    name = s.get_name()
    default_storage.save(name, f)

    compress.delay(name)
    return HttpResponse(status=200)


def list_screenshots(request):
    ss = Screenshot.objects.all().order_by('-time')
    ss = ss[:10]
    data = [(s.get_name(), s.time) for s in ss]
    return render(request, 'screenshots.html', {'data': data})

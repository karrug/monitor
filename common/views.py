import uuid
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login

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
        return HttpResponse('Failed to login', status=401)

    s = Screenshot.objects.create(user=u)

    f = request.FILES['file']
    name = s.get_name()
    default_storage.save(name, f)

    compress.delay(name)
    return HttpResponse(status=200)


@login_required
def list_screenshots(request):
    ss = Screenshot.objects.filter(user=request.user).order_by('-time')
    paginator = Paginator(ss, 10)
    page = request.GET.get('page')
    data = paginator.get_page(page)
    return render(request, 'screenshots.html', {'data': data})


def signup(request):
    if request.method == 'POST':
        n = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        u = User.objects.create(username=n, email=e, password=p)
        next = request.GET.get('next', reverse('list_screenshots'))
        return HttpResponseRedirect(next)
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        n = request.POST['username']
        p = request.POST['password']
        u = authenticate(username=n, password=p)
        if u:
            login(request, u)
            next = request.GET.get('next', reverse('list_screenshots'))
            return HttpResponseRedirect(next)
        else:
            return HttpResponse(status=401)
    return render(request, 'signin.html')

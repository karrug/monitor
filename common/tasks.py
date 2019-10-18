from __future__ import absolute_import, unicode_literals
import sh
import subprocess

from celery import shared_task
from django.conf import settings


@shared_task
def compress(name):
    mp = settings.MEDIA_ROOT
    src = '%s/%s' % (mp, name)
    i = '%s/%s.jpg' % (mp, name)
    sh.convert(src, i)
    dst = '%s/compressed/%s.jpg' % (mp, name)
    cmd = '/opt/mozjpeg/bin/cjpeg -quality 10 %s > %s' % (i, dst)
    subprocess.check_call(cmd, shell=True)
    sh.rm(src)
    sh.rm(i)

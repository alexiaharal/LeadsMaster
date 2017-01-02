# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour=14, minute=25))
def every_day_midnight():
    print("This is run every Monday morning at 7:30")


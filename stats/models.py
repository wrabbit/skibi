from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.conf import settings
# Create your models here.


class Stat(models.Model):
    ip = models.IPAddressField()
    referer = models.CharField(max_length=50)
    date = models.DateTimeField()



class UserActivity(models.Model):
    user = models.ForeignKey(User,null=True, blank=True,db_index=True)
    session = models.ForeignKey(Session,db_index=True,null=True, blank=True)
    date = models.DateTimeField(help_text="Date Request started processing",auto_now_add=True,db_index=True)
    request_time = models.IntegerField(help_text="Processing time (in ms)",null=True, blank=True)
    request_url = models.CharField(max_length=800,db_index=True)
    referer_url = models.URLField(verify_exists=False,db_index=True,blank=True, null=True)
    client_address = models.IPAddressField(blank=True,null=True)
    client_host = models.CharField(max_length=256,blank=True,null=True)
    browser_info = models.TextField(null=True,blank=True)
    error = models.TextField(null=True,blank=True)
       

    #class Meta:
    #    unique_together = (("request_url", "session"),)

    def set_request_time(self):
        from datetime import datetime
        self.request_time = (datetime.now() -  self.date ).microseconds

        if self.request_url is not settings.LOGIN_URL:
            try:
                self.save()
            except:
                return False



from django.db import models

import eventCalBase

class EventCalendar(models.Model):
    class Admin:
        pass

    owner = models.CharField(maxlength=50)
    year = models.IntegerField()
    month = models.IntegerField()

    class Meta:
        unique_together = (('owner', 'year', 'month'),)
    
    def __str__(self):
        return 'of %s for %02d/%04d' % (
                self.owner, self.month, self.year)


class Event(models.Model):
    class Admin:
        pass

    name =  models.CharField(maxlength=50)
    desc =  models.CharField(maxlength=200)
    when =  models.DateTimeField('When the event begin')
    cal  =  models.ForeignKey(EventCalendar)

    def __str__(self):
        return '%s @ %s' % (self.name, self.when)



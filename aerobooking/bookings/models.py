from django.db import models
from django.shortcuts import reverse
from members.models import Member
import datetime

# Create your models here.

def date_default():
    return datetime.datetime.now()


class Aircraft(models.Model):
    _callsign = models.CharField(max_length=20, db_column='callsign')
    _slug = models.CharField(max_length=20, db_column='slug', null=True)

    @property  # getter for callsign property
    def callsign(self):
        return self._callsign

    @callsign.setter
    def callsign(self, value):
        self._callsign = value
        svalue = ''.join( (filter(lambda x: x.isalnum(), value)) ).lower()
        slug = svalue[-2:]
        if Aircraft.objects.filter(_slug=slug).count():
            slug = svalue[-4:]
        if Aircraft.objects.filter(_slug=slug).count():
            slug = svalue
        self._slug = slug

    @property
    def slug(self):
        return self._slug

    @classmethod
    def get_by_slug(klass, slug):
        try:
            return klass.objects.get(_slug = slug)
        except:
            return None

    def __str__(self):
        return self.callsign


class Booking(models.Model):
    date = models.DateField(default=date_default)
    start_time = models.PositiveSmallIntegerField(default=1230)
    duration = models.PositiveSmallIntegerField(default=120)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=1,
        choices=[('T', 'Instruction'), ('P', 'Private Hire')],
        default='T')
    remarks = models.CharField(max_length=500, default='', blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    authorised = models.BooleanField(default=False)

    class Meta:
        ordering = ('date', 'start_time', 'aircraft')

    @property
    def slug(self):
        return f"{self.date}-{self.start_time:04d}-{self.aircraft.slug.lower()}"

    @classmethod
    def get_by_slug(klass, slug):
        sd = slug.split('-')
        try:
            slugdate = datetime.date(int(sd[0]), int(sd[1]), int(sd[2]))
        except:
            slugdate = datetime.date.today()
        try:
            slugtime = int(sd[3])
        except:
            slugtime = 1230
        if len(sd) > 4:
            slugaircraft = Aircraft.get_by_slug(sd[4])
        else:
            slugaircraft = None
        try:
            booking = klass.objects.filter(date=slugdate, start_time=slugtime, aircraft=slugaircraft)[0]
        except:
            booking = None
        return booking

    def get_absolute_url(self):
        return reverse('bookings_edit', args=[self.slug])

    @classmethod
    def get_form_url(klass, date, time, aircraft):
        return reverse('bookings_create') + f"?date={date}&time={time // 60 * 100 + time % 60:04d}&aircraft={aircraft.slug}"


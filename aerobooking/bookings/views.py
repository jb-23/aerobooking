from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

from .models import Booking, Aircraft
from .forms import BookingUserForm, BookingAdminForm
from members.models import Member

# Create your views here.


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


def home(request):
    context = {
        'user': request.user,
    }
    return render(request, 'home.html', context)

def bookings(request):
    if request.method == 'POST':
        return bookings_edit(request)
    return bookings_table(request)

@login_required(redirect_field_name='')
def bookings_table(request):
    context = {
      'user': request.user,
    }
    return render(request, 'bookings-table.html', context)

@login_required(redirect_field_name='')
def bookings_list(request):
    data = []
    requested_data = []
    if request.user.is_staff:
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.filter(member=request.user)
    for b in bookings.order_by('-date', 'start_time', 'aircraft'):
        start_time = b.start_time // 100 * 60 + b.start_time % 100
        finish_time = start_time + b.duration
        d = {
            'date': b.date,
            'aircraft': b.aircraft.callsign,
            'start_time': f"{start_time // 60:02d}:{start_time % 60:02d}",
            'finish_time': f"{finish_time // 60:02d}:{finish_time % 60:02d}",
            'type': b.type,
            'remarks': b.remarks,
            'member': b.member.username,
            'authorised': b.authorised,
            'link': reverse('bookings_edit', args=[b.slug]),
        }
        data.append(d)
        if not b.authorised:
            requested_data.append(d)
    context = {
        'bookings': data,
        'requested_bookings': requested_data,
        'user': request.user,
    }
    return render(request, 'bookings-list.html', context)

@login_required(redirect_field_name='')
def bookings_edit(request, slug=None):
    booking = None
    if slug:
        booking = Booking.get_by_slug(slug)
        if not request.user.is_staff:
            if booking.member != request.user:
                booking = None
                slug = None
    if not booking:
        rdate = request.GET.get('date', False)
        rtime = request.GET.get('time', False)
        racft = request.GET.get('aircraft', False)
        booking = Booking()
        if request.user.is_staff:
            booking.authorised = True
        if rdate:
            rdate = rdate.split('-')
            try:
                booking.date = datetime.date(int(rdate[0]), int(rdate[1]), int(rdate[2]))
            except:
                pass
        if rtime:
            booking.start_time = int(rtime)
        if racft:
            try:
                booking.aircraft = Aircraft.objects.get(_slug=racft)
            except:
                pass
    if request.method == 'POST':
        if request.POST.get('_method', "").lower() == "delete":
            booking.delete()
            return HttpResponseSeeOther(get_bookingview_url(date=booking.date))
        else:
            form = update_booking(booking, request)
            if not form:
                return HttpResponseSeeOther(get_bookingview_url(date=booking.date))
    else:
        start_time = booking.start_time
        start_time = start_time // 100 * 60 + start_time % 100
        finish_time = start_time + booking.duration
        finish_time = finish_time // 60 * 100 + finish_time % 60
        form = ( BookingAdminForm(initial={'finish_time': finish_time},
            instance=booking) if request.user.is_staff else
            BookingUserForm(initial={'finish_time': finish_time},
            instance=booking) )
    context = {
        'user': request.user,
        'form': form,
        'action': reverse('bookings_edit', args=[slug]) if slug else reverse('bookings'),
        'submit_text': "Update Booking" if slug else "Create Booking",
        'cancel_text': "Cancel Booking" if slug else "",
    }
    return render(request, 'booking-details.html', context)

def update_booking(booking, request):
    form = BookingAdminForm(request.POST) if request.user.is_staff else BookingUserForm(request.POST)
    if not form.is_valid():
        return form
    # admin only
    if request.user.is_staff:
        member_no = int(request.POST.get('member'))
        authorised = True if request.POST.get('authorised', False) else False
    else:
        member_no = request.user.pk
        authorised = False
    #
    booking.date = request.POST.get('date')
    start_time = int(request.POST.get('start_time'))
    finish_time = int(request.POST.get('finish_time'))
    booking.start_time = start_time
    start_time = start_time // 100 * 60 + start_time % 100
    finish_time = finish_time // 100 * 60 + finish_time % 100
    duration = finish_time - start_time
    # check for time error
    if duration <= 0:
        form.add_error(None, ValidationError("Finish time must be after start time."))
        return form
    booking.duration = duration
    booking.aircraft = Aircraft.objects.get(pk=int(request.POST.get('aircraft')))
    booking.type = request.POST.get('type')
    booking.remarks = request.POST.get('remarks')
    booking.member = Member.objects.get(id=member_no)
    booking.authorised = authorised
    # check for booking collision
    others = Booking.objects.filter(date=booking.date, aircraft=booking.aircraft)
    for b in others:
        if b.pk == booking.pk:
            continue
        st = b.start_time
        st = st // 100 * 60 + st % 100
        ft = st + b.duration
        if ((st < start_time and ft > start_time)
                or (st >= start_time and st < finish_time)):
            form.add_error(None, ValidationError(
                "Aircraft is already booked at these times."
                + " Please choose a different aircraft, flight times or date."
                ))
            return form
    booking.save()
    return None

def get_bookingview_url(*, date=False):
    return reverse('main') + (f"?date={date}" if date else "")

def about(request):
    context = {
        'user': request.user,
    }
    return render(request, 'about.html', context)

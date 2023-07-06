from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Book
from django.core.mail import EmailMessage
import datetime
from django.template  import Context
from django.template.loader import render_to_string,get_template
from django.conf import settings

class HTV(TemplateView):
    template_name = "home.html"



class booking(TemplateView):
    template_name = "reservation.html"
    def post(self,request):
        fname=request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        book=Book.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,

        )
        book.save()

        messages.add_message(request,messages.SUCCESS,f"درخواست رزرو داده شد.نوبت شما ایمیل خواهد شد")
        return HttpResponseRedirect(request.path)


class Manage(TemplateView):
    template_name = "manage.html"
    login_required = True;

    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Book.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "نوبت لیزر",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f" نوبت رزرو شد")
        return HttpResponseRedirect(request.path)

    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        appointments = Book.objects.all()
        context.update({
            "appointments":appointments,
            "title":"Manage Appointments"

        })
        return context

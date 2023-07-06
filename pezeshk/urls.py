from django.urls import path
from .views import HTV,booking,Manage

urlpatterns=[
    path("",HTV.as_view(),name="home"),
    path("make-an-appointment/", booking.as_view(), name="appointment"),
    path("manage-appointments/", Manage.as_view(), name="manage")
]
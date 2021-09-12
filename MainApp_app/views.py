from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from MainApp_app.EmailBackEnd import EmailBackEnd


def ShowLoginPage(request):
    return render(request, "login_template.html")


def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "3":
                return HttpResponse("Tutor login")
            elif user.user_type == "4":
                return HttpResponse("Student login")
            else:
                messages.error(request, "Invalid Login Details")
                return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def DoLogout(request):
    logout(request)
    return HttpResponseRedirect("/")

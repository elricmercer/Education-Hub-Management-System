import datetime
import random
import string

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from MainApp_app.Forms import EditProfileForm
from MainApp_app.models import Admin, SuperUser


# DASHBOARD SECTION
def Dashboard(request):
    return render(request, "Admin_Pages/dashboard_template.html")


# END OF DASHBOARD SECTION


# PROFILE SECTION
def Profile(request):
    admin = Admin.objects.get(super_id=request.user.id)
    role = ""
    if request.user.user_type == "1":
        role = "Super User"
    elif request.user.user_type == "2":
        role = "Administrator"
    context = {"admin": admin, "role": role}
    return render(request, "Admin_Pages/profile_template.html", context)


def EditProfile(request):
    admin = Admin.objects.get(super_id=request.user.id)
    form = EditProfileForm()
    form.fields['username'].initial = request.user.username
    form.fields['email'].initial = request.user.email
    form.fields['firstName'].initial = request.user.first_name
    form.fields['lastName'].initial = request.user.last_name
    form.fields['gender'].initial = admin.gender
    form.fields['dob'].initial = admin.dob
    form.fields['phoneNo'].initial = admin.phone_no
    request.session['username'] = request.user.username
    context = {"form": form}
    return render(request, "Admin_Pages/edit_admin_profile_template.html", context)


def SaveEditProfile(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        currentUsername = request.session['username']
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            firstName = form.cleaned_data["firstName"]
            lastName = form.cleaned_data["lastName"]
            gender = form.cleaned_data["gender"]
            dob = form.cleaned_data["dob"]
            phoneNo = form.cleaned_data["phoneNo"]
            profilePic = request.FILES['profilePic']
            fs = FileSystemStorage()
            filename = fs.save(profilePic.name, profilePic)
            profilePicUrl = fs.url(filename)
            superUserCheck = SuperUser.objects.all()
            for sup in superUserCheck:
                if username == sup.username:
                    if username == currentUsername:
                        pass
                    else:
                        messages.error(request, "Error! Username already taken")
                        return HttpResponseRedirect(reverse("admin_edit_profile"))
            try:
                superUser = SuperUser.objects.get(id=request.user.id)
                admin = Admin.objects.get(super_id=request.user.id)
                superUser.username = username
                superUser.email = email
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.save()
                admin.gender = gender
                admin.dob = dob
                admin.phone_no = phoneNo
                admin.pic = profilePicUrl
                admin.save()
                try:
                    del request.session['username']
                except:
                    pass
                messages.success(request, "Edited")
                return HttpResponseRedirect(reverse("admin_edit_profile"))
            except:
                try:
                    del request.session['username']
                except:
                    pass
                messages.error(request, "Failed")
                return HttpResponseRedirect(reverse("admin_edit_profile"))
        else:
            try:
                del request.session['username']
            except:
                pass
            context = {"form": form}
            messages.error(request, "Failed")
            return render(request, "Admin_Pages/edit_admin_profile_template.html", context)
# END OF PROFILE SECTION

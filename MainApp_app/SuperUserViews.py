import datetime

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from MainApp_app.models import Admin, SuperUser, CompanyEarnings, Student


# ADMINISTRATORS SECTION
def ViewAdministrators(request):
    admin = Admin.objects.all()
    superUser = SuperUser.objects.filter(user_type="2").order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(superUser, 6)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {"admin": admin, "users": users}

    return render(request, "Super_User_Pages/view_administrators_template.html", context)


def SaveAddAdmin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax:
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confPassword = request.POST.get("confPassword")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            adminCheck = Admin.objects.all()
            superUserCheck = SuperUser.objects.all()

            if firstName.isalpha():
                pass
            else:
                return HttpResponse("firstName")

            if lastName.isalpha():
                pass
            else:
                return HttpResponse("lastName")

            for sup in superUserCheck:
                if username == sup.username:
                    return HttpResponse("username")

            for sup in superUserCheck:
                if email == sup.email:
                    return HttpResponse("email")

            if password != confPassword:
                return HttpResponse("confPassword")

            for adCheck in adminCheck:
                if phoneNo == adCheck.phone_no:
                    return HttpResponse("phoneNo")

            if phoneNo.isnumeric():
                pass
            else:
                return HttpResponse("phoneNo2")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo3")

            try:
                superUser = SuperUser.objects.create_user(username=username, first_name=firstName, last_name=lastName,
                                                          email=email,
                                                          password=password, user_type="2")
                superUser.save()
                admin = Admin(gender=gender, dob=dob, phone_no=phoneNo, super_id=superUser.id)
                admin.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To add")
            return HttpResponseRedirect(reverse("admin_view_administrators"))


def EditAdmin(request, superID):
    superUser = SuperUser.objects.get(id=superID)
    adminUser = Admin.objects.get(super_id=superID)
    context = {"superUser": superUser, "adminUser": adminUser}
    return render(request, "Super_User_Pages/edit_admin_template.html", context)


def SaveEditAdmin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            currentUsername = request.POST.get("currentUsername")
            currentEmail = request.POST.get("currentEmail")
            currentPhoneNo = request.POST.get("currentPhoneNo")
            adminSuperID = request.POST.get("adminSuperID")
            superUserAll = SuperUser.objects.all()
            adminUserAll = Admin.objects.all()

            if firstName.isalpha():
                pass
            else:
                return HttpResponse("firstName")

            if lastName.isalpha():
                pass
            else:
                return HttpResponse("lastName")

            for sup in superUserAll:
                if username == sup.username:
                    if username == currentUsername:
                        pass
                    else:
                        return HttpResponse("username")

            for sup in superUserAll:
                if email == sup.email:
                    if email == currentEmail:
                        pass
                    else:
                        return HttpResponse("email")

            for ad in adminUserAll:
                if phoneNo == ad.phone_no:
                    if phoneNo == currentPhoneNo:
                        pass
                    else:
                        return HttpResponse("phoneNo")

            if phoneNo.isnumeric():
                pass
            else:
                return HttpResponse("phoneNo2")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo3")

            try:
                superUser = SuperUser.objects.get(id=adminSuperID)
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.username = username
                superUser.email = email
                superUser.save()
                adminUser = Admin.objects.get(super_id=adminSuperID)
                adminUser.gender = gender
                adminUser.dob = dob
                adminUser.phone_no = phoneNo
                adminUser.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To edit")
            return HttpResponseRedirect(reverse("admin_view_administrators"))


def DeleteAdmin(request, superUserID):
    try:
        superUser = SuperUser.objects.filter(id=superUserID).delete()
        messages.success(request, "Deleted")
        return HttpResponseRedirect(reverse("admin_view_administrators"))
    except:
        messages.error(request, "Failed! To delete")
        return HttpResponseRedirect(reverse("admin_view_administrators"))
# END OF ADMINISTRATORS SECTION


# REVENUE SECTION
def ViewRevenue(requests):
    earned = CompanyEarnings.objects.all().order_by('-created_at')
    allYearList = []
    yearsList = []

    for earn in earned:
        year = int(earn.year)
        allYearList.append(year)

    try:
        earliestYear = min(allYearList)
        currentDate = datetime.date.today()
        currentYear = currentDate.year
        diff = (currentYear - earliestYear) + 1

        for i in range(diff):
            years = str(earliestYear + i)
            yearsList.append(years)
    except:
        pass

    page = requests.GET.get('page', 1)
    paginator = Paginator(earned, 6)

    try:
        earnings = paginator.page(page)
    except PageNotAnInteger:
        earnings = Paginator.page(1)
    except EmptyPage:
        earnings = paginator.page(paginator.num_pages)

    yearsList.sort(reverse=True)
    context = {"earnings": earnings, "yearsList": yearsList}
    return render(requests, "Super_User_Pages/view_revenue_template.html", context)
# END OF REVENUE SECTION
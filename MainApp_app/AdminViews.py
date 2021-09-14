import datetime
import json
import os
import random
import string

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Education_Hub_Management_System.settings import BASE_DIR
from MainApp_app.models import Admin, SuperUser, Student, StudentPayment, Tutor, TutorEarnings


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


def EditProfile(request):  # CHANGE THIS TO MODAL
    admin = Admin.objects.get(super_id=request.user.id)
    context = {"admin": admin}
    return render(request, "Admin_Pages/edit_admin_profile_template.html", context)


def SaveEditProfile(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax:
            currentUsername = request.POST.get("currentUsername")
            currentPhoneNo = request.POST.get("currentPhoneNo")
            currentEmail = request.POST.get("currentEmail")
            username = request.POST.get("username")
            email = request.POST.get("email")
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            superUser = SuperUser.objects.all()
            adminUser = Admin.objects.all()

            for sup in superUser:
                if username == sup.username:
                    if username == currentUsername:
                        pass
                    else:
                        return HttpResponse("username")

            for sup in superUser:
                if email == sup.email:
                    if email == currentEmail:
                        pass
                    else:
                        return HttpResponse("email")

            if firstName.isalpha():
                pass
            else:
                return HttpResponse("firstName")

            if lastName.isalpha():
                pass
            else:
                return HttpResponse("lastName")

            for ad in adminUser:
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
                admin.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")

        else:
            messages.error(request, "Failed!")
            return HttpResponseRedirect(reverse("admin_edit_profile"))


def SaveProfilePic(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        profilePic = request.FILES['profilePic']
        fs = FileSystemStorage()
        filename = fs.save(profilePic.name, profilePic)
        profilePicUrl = fs.url(filename)

        try:
            admin = Admin.objects.get(super_id=request.user.id)
            admin.pic = profilePicUrl
            admin.save()
            messages.success(request, "Uploaded")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Upload")
            return HttpResponseRedirect(reverse("admin_profile"))


def RemoveProfilePic(request):
    admin = Admin.objects.get(super_id=request.user.id)

    if admin.pic is not None or admin.pic != "":
        if os.path.exists(str(BASE_DIR) + "" + str(admin.pic)):
            try:
                os.remove(str(BASE_DIR) + "" + str(admin.pic))
                admin.pic = ""
                admin.save()
                messages.success(request, "Removed")
                return HttpResponseRedirect(reverse("admin_profile"))
            except:
                messages.error(request, "Failed to Remove")
                return HttpResponseRedirect(reverse("admin_profile"))

    messages.error(request, "Failed to Remove")
    return HttpResponseRedirect(reverse("admin_profile"))


# END OF PROFILE SECTION


# ADMINISTRATORS SECTION (FOR SUPER USER ONLY)
def ViewAdministrators(request):
    admin = Admin.objects.all()
    superUser = SuperUser.objects.filter(user_type="2")
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


# STUDENT SECTION
def ViewStudents(request):
    student = Student.objects.all()
    superUser = SuperUser.objects.filter(user_type="4")
    page = request.GET.get('page', 1)
    paginator = Paginator(superUser, 6)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {"student": student, "users": users}
    return render(request, "Admin_Pages/view_students_template.html", context)


def SaveAddStudent(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confPassword = request.POST.get("confPassword")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
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

            if phoneNo.isnumeric():
                pass
            else:
                return HttpResponse("phoneNo")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo2")

            try:
                superUser = SuperUser.objects.create_user(username=username, first_name=firstName, last_name=lastName,
                                                          email=email,
                                                          password=password, user_type="4")
                superUser.save()
                student = Student(gender=gender, dob=dob, phone_no=phoneNo, super_id=superUser.id)
                student.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To add")
            return HttpResponseRedirect(reverse(""))


def EditStudent(request, superID):
    superUser = SuperUser.objects.get(id=superID)
    student = Student.objects.get(super_id=superID)
    context = {"superUser": superUser, "student": student, "id": superID}
    return render(request, "Admin_Pages/edit_student_template.html", context)


def SaveEditStudent(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        studSuperID = request.POST.get("studentSuperID")
        if request.is_ajax():
            studentSuperID = request.POST.get("studentSuperID")
            currentUsername = request.POST.get("currentUsername")
            currentEmail = request.POST.get("currentEmail")
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            superUserCheck = SuperUser.objects.all()

            if firstName.isalpha():
                pass
            else:
                return HttpResponse("firstName")

            if lastName.isalpha():
                pass
            else:
                return HttpResponse("lastName")

            for supCheck in superUserCheck:
                if username == supCheck.username:
                    if username == currentUsername:
                        pass
                    else:
                        return HttpResponse("username")

            for supCheck in superUserCheck:
                if email == supCheck.email:
                    if email == currentEmail:
                        pass
                    else:
                        return HttpResponse("email")

            if phoneNo.isnumeric():
                pass
            else:
                return HttpResponse("phoneNo")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo2")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo2")

            try:
                superUser = SuperUser.objects.get(id=studentSuperID)
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.username = username
                superUser.email = email
                superUser.save()
                student = Student.objects.get(super_id=studentSuperID)
                student.gender = gender
                student.dob = dob
                student.phone_no = phoneNo
                student.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")

        else:
            messages.error(request, "Failed! To edit")
            return HttpResponseRedirect(reverse("admin_edit_students", kwargs={"superID": studSuperID}))


def DeleteStudent(request, superID):
    try:
        superUser = SuperUser.objects.filter(id=superID).delete()
        messages.success(request, "Deleted")
        return HttpResponseRedirect(reverse("admin_view_students"))
    except:
        messages.error(request, "Failed! To delete")
        return HttpResponseRedirect(reverse("admin_view_students"))


def SearchStudentPayment(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            studentID = request.POST.get("studentID")
            student = Student.objects.all()
            exists = False

            for stud in student:
                if studentID == str(stud.id):
                    exists = True
                    break

            if not exists:
                response = {'status': 0}
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                response = {'status': 1, 'url': reverse("admin_view_student_payment", kwargs={"studID": studentID})}
                return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            messages.error(request, "Failed! To search")
            return HttpResponseRedirect(reverse("admin_view_students"))


def ViewStudentPayment(request, studID):
    student = Student.objects.get(id=studID)
    superUser = SuperUser.objects.get(id=student.super_id)
    pay = StudentPayment.objects.filter(student_id=studID)
    page = request.GET.get('page', 1)
    paginator = Paginator(pay, 6)

    try:
        pays = paginator.page(page)
    except PageNotAnInteger:
        pays = paginator.page(1)
    except EmptyPage:
        pays = paginator.page(paginator.num_pages)

    context = {"student": student, "superUser": superUser, "pays": pays, "id": studID}
    return render(request, "Admin_Pages/view_student_payments_template.html", context)


# END OF STUDENT SECTION


# TUTOR SECTION
def ViewTutors(request):
    tutor = Tutor.objects.all()
    superUser = SuperUser.objects.filter(user_type="3")
    page = request.GET.get('page', 1)
    paginator = Paginator(superUser, 6)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {"tutor": tutor, "users": users}
    return render(request, "Admin_Pages/view_tutors_template.html", context)


def SaveAddTutor(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confPassword = request.POST.get("confPassword")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            superUserCheck = SuperUser.objects.all()
            tutorCheck = Tutor.objects.all()

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

            if phoneNo.isnumeric():
                pass
            else:
                return HttpResponse("phoneNo")

            if len(phoneNo) >= 10:
                pass
            else:
                return HttpResponse("phoneNo2")

            for tut in tutorCheck:
                if phoneNo == tut.phone_no:
                    return HttpResponse("phoneNo3")

            try:
                superUser = SuperUser.objects.create_user(username=username, first_name=firstName, last_name=lastName,
                                                          email=email,
                                                          password=password, user_type="3")
                superUser.save()
                tutor = Tutor(gender=gender, dob=dob, phone_no=phoneNo, super_id=superUser.id)
                tutor.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To add")
            return HttpResponseRedirect(reverse("admin_view_tutors"))


def DeleteTutor(request, superID):
    try:
        superUser = SuperUser.objects.filter(id=superID).delete()
        messages.success(request, "Deleted")
        return HttpResponseRedirect(reverse("admin_view_tutors"))
    except:
        messages.error(request, "Failed! To delete")
        return HttpResponseRedirect(reverse("admin_view_tutors"))


def EditTutor(request, superID):
    superUser = SuperUser.objects.get(id=superID)
    tutor = Tutor.objects.get(super_id=superID)
    context = {"superUser": superUser, "tutor": tutor, "id": superID}
    return render(request, "Admin_Pages/edit_tutor_template.html", context)


def SaveEditTutor(request):
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
            tutorSuperID = request.POST.get("tutorSuperID")
            superUserAll = SuperUser.objects.all()
            tutorUserAll = Tutor.objects.all()

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

            for tut in tutorUserAll:
                if phoneNo == tut.phone_no:
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
                superUser = SuperUser.objects.get(id=tutorSuperID)
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.username = username
                superUser.email = email
                superUser.save()
                tutor = Tutor.objects.get(super_id=tutorSuperID)
                tutor.gender = gender
                tutor.dob = dob
                tutor.phone_no = phoneNo
                tutor.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To edit")
            return HttpResponseRedirect(reverse("admin_view_tutors"))


def SearchTutorPayment(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            tutorID = request.POST.get("tutorID")
            tutor = Tutor.objects.all()
            exists = False

            for tut in tutor:
                if tutorID == str(tut.id):
                    exists = True
                    break

            if not exists:
                response = {'status': 0}
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                response = {'status': 1, 'url': reverse("admin_view_tutor_payment", kwargs={"tutorID": tutorID})}
                return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            messages.error(request, "Failed! To search")
            return HttpResponseRedirect(reverse("admin_view_tutors"))


def ViewTutorPayment(request, tutorID):
    tutor = Tutor.objects.get(id=tutorID)
    superUser = SuperUser.objects.get(id=tutor.super_id)
    pay = TutorEarnings.objects.filter(tutor_id=tutorID)
    page = request.GET.get('page', 1)
    paginator = Paginator(pay, 6)

    try:
        pays = paginator.page(page)
    except PageNotAnInteger:
        pays = paginator.page(1)
    except EmptyPage:
        pays = paginator.page(paginator.num_pages)

    context = {"tutor": tutor, "superUser": superUser, "pays": pays, "id": tutorID}
    return render(request, "Admin_Pages/view_tutor_payment_template.html", context)
# END OF TUTOR SECTION

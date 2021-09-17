import os

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Education_Hub_Management_System.settings import BASE_DIR
from MainApp_app.models import Tutor, SuperUser, EnrolledStudents, Enrollment, Student, EnrollmentDays, EnrollmentTime, \
    Course, TutorsCertifiedToCourse, Schedule


# DASHBOARD SECTION
def Dashboard(request):
    return render(request, "Tutor_Pages/dashboard_template.html")


# END OF DASHBOARD SECTION


# PROFILE SECTION
def Profile(request):
    superUser = SuperUser.objects.get(id=request.user.id)
    tutor = Tutor.objects.get(super_id=superUser.id)
    role = "Tutor"
    context = {"superUser": superUser, "tutor": tutor, "role": role}
    return render(request, "Tutor_Pages/profile_template.html", context)


def SaveProfilePic(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        profilePic = request.FILES['profilePic']
        fs = FileSystemStorage()
        filename = fs.save(profilePic.name, profilePic)
        profilePicUrl = fs.url(filename)

        try:
            tutor = Tutor.objects.get(super_id=request.user.id)
            tutor.pic = profilePicUrl
            tutor.save()
            messages.success(request, "Uploaded")
            return HttpResponseRedirect(reverse("tutor_profile"))
        except:
            messages.error(request, "Failed to Upload")
            return HttpResponseRedirect(reverse("tutor_profile"))


def RemoveProfilePic(request):
    tutor = Tutor.objects.get(super_id=request.user.id)

    if tutor.pic is not None or tutor.pic != "":
        if os.path.exists(str(BASE_DIR) + "" + str(tutor.pic)):
            try:
                os.remove(str(BASE_DIR) + "" + str(tutor.pic))
                tutor.pic = ""
                tutor.save()
                messages.success(request, "Removed")
                return HttpResponseRedirect(reverse("tutor_profile"))
            except:
                messages.error(request, "Failed to Remove")
                return HttpResponseRedirect(reverse("tutor_profile"))

    messages.error(request, "Failed to Remove")
    return HttpResponseRedirect(reverse("tutor_profile"))


def EditProfile(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    context = {"tutor": tutor}
    return render(request, "Tutor_Pages/edit_profile_template.html", context)


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
            tutorUser = Tutor.objects.all()

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

            for tut in tutorUser:
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
                superUser = SuperUser.objects.get(id=request.user.id)
                tutor = Tutor.objects.get(super_id=request.user.id)
                superUser.username = username
                superUser.email = email
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.save()
                tutor.gender = gender
                tutor.dob = dob
                tutor.phone_no = phoneNo
                tutor.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")

        else:
            messages.error(request, "Failed!")
            return HttpResponseRedirect(reverse("tutor_edit_profile"))


# END OF PROFILE SECTION


# STUDENT SECTION
def ViewStudents(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    enollStudents = EnrolledStudents.objects.all()
    enoll = Enrollment.objects.filter(tutor_id=tutor.id)
    students = Student.objects.all()
    superUser = SuperUser.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(enollStudents, 6)

    try:
        enollStuds = paginator.page(page)
    except PageNotAnInteger:
        enollStuds = paginator.page(1)
    except EmptyPage:
        enollStuds = paginator.page(paginator.num_pages)

    context = {"students": students, "enollStuds": enollStuds, "superUser": superUser, "enoll": enoll}
    return render(request, "Tutor_Pages/view_students_template.html", context)
# END OF STUDENT SECTION


# CLASSES SECTION
def ViewClasses(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    enrollment = Enrollment.objects.filter(tutor_id=tutor.id)
    enrollmentStuds = EnrolledStudents.objects.all()
    enrollmentDays = EnrollmentDays.objects.all()
    enrollmentTime = EnrollmentTime.objects.all()
    student = Student.objects.all()
    superUser = SuperUser.objects.all()
    course = Course.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(enrollment, 6)

    try:
        enrollments = paginator.page(page)
    except PageNotAnInteger:
        enrollments = paginator.page(1)
    except EmptyPage:
        enrollments = paginator.page(paginator.num_pages)

    context = {"enrollments": enrollments, "enrollmentStuds": enrollmentStuds, "enrollmentDays": enrollmentDays,
               "enrollmentTime": enrollmentTime, "student": student, "superUser": superUser, "course": course}
    return render(request, "Tutor_Pages/view_classes_template.html", context)
# END OF CLASSES SECTION


# SCHEDULES SECTION
def ViewSchedule(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    certified = TutorsCertifiedToCourse.objects.filter(tutor_id=tutor.id)
    course = Course.objects.all()
    schedule = Schedule.objects.filter(tutor_id=tutor.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(schedule, 6)

    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    context = {"schedules": schedules, "certified": certified, "course": course}
    return render(request, "Tutor_Pages/view_schedules_template.html", context)


def SaveSchedule(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            courseID = request.POST.get("courseID")
            duration = request.POST.get("duration")
            day = request.POST.get("day")
            time = request.POST.get("time")
            status = request.POST.get("status")
            tutor = Tutor.objects.get(super_id=request.user.id)

            try:
                schedule = Schedule(course_id=courseID, duration=duration, day=day, time=time, status=status, tutor_id=tutor.id)
                schedule.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To add")
            return HttpResponseRedirect(reverse("tutor_view_schedules"))


def EditSchedule(request, schID):
    schedule = Schedule.objects.get(id=schID)
    context = {"schedule": schedule, "id": schID, }
    return render(request, "Tutor_Pages/edit_schedule_template.html", context)


def SaveEditSchedule(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            scheduleID = request.POST.get("scheduleID")
            duration = request.POST.get("duration")
            day = request.POST.get("day")
            time = request.POST.get("time")
            status = request.POST.get("status")

            try:
                schedule = Schedule.objects.get(id=scheduleID)
                schedule.duration = duration
                schedule.day = day
                schedule.time = time
                schedule.status = status
                schedule.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! to edit")
            return HttpResponseRedirect(reverse("tutor_view_schedules"))


def DeleteSchedule(request, schID):
    try:
        schedule = Schedule.objects.filter(id=schID).delete()
        messages.success(request, "Deleted")
        return HttpResponseRedirect(reverse("tutor_view_schedules"))
    except:
        messages.error(request, "Failed! To delete")
        return HttpResponseRedirect(reverse("tutor_view_schedules"))
# END OF SCHEDULES

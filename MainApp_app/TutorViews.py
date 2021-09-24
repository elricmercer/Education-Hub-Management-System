import datetime
import json
import os

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Education_Hub_Management_System.settings import BASE_DIR
from MainApp_app.models import Tutor, SuperUser, EnrolledStudents, Enrollment, Student, EnrollmentDays, EnrollmentTime, \
    Course, TutorsCertifiedToCourse, Schedule, TutorApplyToCertifyToCourse, TutorEarnings, ContactUs, Admin, Attendance, \
    AttendanceStudent, AttendancePercent


# DASHBOARD SECTION
def Dashboard(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    enrollment = Enrollment.objects.filter(tutor_id=tutor.id)
    enrollmentStuds = EnrolledStudents.objects.all()
    studentList = []

    for enroll in enrollment:
        for enrollStuds in enrollmentStuds:
            if enroll.id == enrollStuds.enrollment_id:
                studentList.append(enrollStuds.student_id)

    uniqueVals = set(studentList)
    totalStudents = len(uniqueVals)
    totalSchedules = Schedule.objects.filter(tutor_id=tutor.id).count()
    totalClasses = Enrollment.objects.filter(tutor_id=tutor.id).count()
    totalCourses = TutorsCertifiedToCourse.objects.filter(tutor_id=tutor.id).count()
    currentDate = datetime.date.today()
    year = str(currentDate.year)

    # SALES CHART
    earnings = TutorEarnings.objects.filter(tutor_id=tutor.id, year=year)
    janTotal = 0
    febTotal = 0
    marTotal = 0
    aprTotal = 0
    mayTotal = 0
    junTotal = 0
    julTotal = 0
    augTotal = 0
    sepTotal = 0
    octTotal = 0
    novTotal = 0
    decTotal = 0

    for earn in earnings:
        if earn.month == "1":
            janTotal = janTotal + float(earn.earned)
        if earn.month == "2":
            febTotal = febTotal + float(earn.earned)
        if earn.month == "3":
            marTotal = marTotal + float(earn.earned)
        if earn.month == "4":
            aprTotal = aprTotal + float(earn.earned)
        if earn.month == "5":
            mayTotal = mayTotal + float(earn.earned)
        if earn.month == "6":
            junTotal = junTotal + float(earn.earned)
        if earn.month == "7":
            julTotal = julTotal + float(earn.earned)
        if earn.month == "8":
            augTotal = augTotal + float(earn.earned)
        if earn.month == "9":
            sepTotal = sepTotal + float(earn.earned)
        if earn.month == "10":
            octTotal = octTotal + float(earn.earned)
        if earn.month == "11":
            novTotal = novTotal + float(earn.earned)
        if earn.month == "12":
            decTotal = decTotal + float(earn.earned)

    context = {"totalStudents": totalStudents, "totalSchedules": totalSchedules, "totalClasses": totalClasses,
               "totalCourses": totalCourses, "year": year, "janTotal": janTotal, "febTotal": febTotal,
               "marTotal": marTotal,
               "aprTotal": aprTotal, "mayTotal": mayTotal, "junTotal": junTotal, "julTotal": julTotal,
               "augTotal": augTotal, "sepTotal": sepTotal, "octTotal": octTotal, "novTotal": novTotal,
               "decTotal": decTotal}

    return render(request, "Tutor_Pages/dashboard_template.html", context)


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
        if os.path.exists(os.path.join(BASE_DIR, str(tutor.pic))):
            try:
                os.remove(os.path.join(BASE_DIR, str(tutor.pic)))
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
    enrollment = Enrollment.objects.filter(tutor_id=tutor.id).order_by('-created_at')
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


@csrf_exempt
def GetStudentsForAttendance(request):
    enrollID = request.POST.get("enrollID")
    startTime = request.POST.get("startTime")
    duration = request.POST.get("duration")
    request.session['enrollID'] = enrollID
    request.session['startTime'] = startTime
    request.session['duration'] = duration
    enrollStudents = EnrolledStudents.objects.filter(enrollment_id=enrollID)
    students = Student.objects.all()
    studentsList = []

    for enroll in enrollStudents:
        for studs in students:
            if enroll.student_id == studs.id:
                studSmallData = {"id": studs.id, "name": studs.super.first_name + " " + studs.super.last_name}
                studentsList.append(studSmallData)

    return JsonResponse(json.dumps(studentsList), content_type="application/json", safe=False)


@csrf_exempt
def SaveStudentAttendance(request):
    enrollID = request.session['enrollID']
    startTime = request.session['startTime']
    duration = request.session['duration']
    currentDate = datetime.date.today()
    enrollment = Enrollment.objects.get(id=enrollID)
    tutorID = enrollment.tutor_id
    studentIDs = request.POST.get("studentIDs")
    studentDataJson = json.loads(studentIDs)
    attendance = Attendance(date=currentDate, start_time=startTime, enrollment_id=enrollID, tutor_id=tutorID,
                            duration=duration)
    attendance.save()

    for studs in studentDataJson:
        attendanceStudent = AttendanceStudent(status=studs['status'], attendance_id=attendance.id,
                                              student_id=studs['id'])
        attendanceStudent.save()

    attendances = Attendance.objects.filter(enrollment_id=enrollID)
    attendancesStud = AttendanceStudent.objects.all()

    for studs2 in studentDataJson:
        present = 0
        absent = 0
        for attend in attendances:
            for attendStud in attendancesStud:
                if attend.id == attendStud.attendance_id:
                    if attendStud.student_id == int(studs2['id']):
                        if attendStud.status == "Present":
                            present = present + 1
                        else:
                            absent = absent + 1
        attendPercent = ((present / (present + absent)) * 100)
        represent = ""
        if attendPercent == 100.0:
            represent = "bg-success"
        elif 80.0 <= attendPercent < 100.0:
            represent = "bg-info"
        elif 50.0 <= attendPercent < 80.0:
            represent = "bg-warning"
        elif attendPercent < 50.0:
            represent = "bg-danger"

        try:
            attendancePercent = AttendancePercent.objects.get(enrollment_id=enrollID, student_id=studs2['id'])
            attendancePercent.percent = attendPercent
            attendancePercent.represent = represent
            attendancePercent.save()
        except:
            attendancePercent2 = AttendancePercent(percent=attendPercent, enrollment_id=enrollID,
                                                   student_id=studs2['id'],
                                                   represent=represent)
            attendancePercent2.save()

    try:
        del request.session['enrollID']
        del request.session['startTime']
        del request.session['duration']
    except:
        pass

    return HttpResponse("ok")


def ViewRecordedAttendance(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            enrollID = request.POST.get("enrollID")
            response = {'url': reverse("tutor_view_marked_attendance", kwargs={"enrollID": enrollID})}
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            messages.error(request, "Failed! To load attendances")
            return HttpResponseRedirect(reverse("tutor_view_classes"))


def ViewMarkedAttendance(request, enrollID):
    tutor = Tutor.objects.get(super_id=request.user.id)
    attendance = Attendance.objects.filter(enrollment_id=enrollID, tutor_id=tutor.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(attendance, 6)

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    context = {"attendances": attendances}
    return render(request, "Tutor_Pages/view_marked_attendance_template.html", context)


def EditAttendance(request, attendID):
    attendanceStud = AttendanceStudent.objects.filter(attendance_id=attendID)
    students = Student.objects.all()
    superUser = SuperUser.objects.all()
    present = "Present"
    absent = "Absent"
    context = {"attendanceStud": attendanceStud, "students": students, "superUser": superUser, "present": present, "absent": absent,
               "id": attendID}
    return render(request, "Tutor_Pages/edit_attendance_template.html", context)


def SaveEditAttendance(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        attendanceID = request.POST.get("attendanceID")
        studentIDs = request.POST.getlist("studentID[]")
        statuses = request.POST.getlist("status[]")
        attendStudents = AttendanceStudent.objects.filter(attendance_id=attendanceID)
        success = False

        for attend in attendStudents:
            for i in range(len(studentIDs)):
                if str(attend.student_id) == studentIDs[i]:
                    try:
                        attend.status = statuses[i]
                        attend.save()
                        attendance = Attendance.objects.get(id=attendanceID)
                        courseTakenID = attendance.enrollment_id
                        attendances = Attendance.objects.filter(enrollment_id=courseTakenID)
                        attendancesStud = AttendanceStudent.objects.all()
                        present = 0
                        absent = 0
                        for attends in attendances:
                            for attendStud in attendancesStud:
                                if attends.id == attendStud.attendance_id:
                                    if attendStud.student_id == int(studentIDs[i]):
                                        if attendStud.status == "Present":
                                            present = present + 1
                                        else:
                                            absent = absent + 1
                        attendPercent = ((present / (present + absent)) * 100)
                        represent = ""
                        if attendPercent == 100.0:
                            represent = "bg-success"
                        elif 80.0 <= attendPercent < 100.0:
                            represent = "bg-info"
                        elif 50.0 <= attendPercent < 80.0:
                            represent = "bg-warning"
                        elif attendPercent < 50.0:
                            represent = "bg-danger"

                        percent = AttendancePercent.objects.get(enrollment_id=courseTakenID, student_id=studentIDs[i])
                        percent.percent = attendPercent
                        percent.represent = represent
                        percent.save()
                        success = True
                    except:
                        messages.error(request, "Failed to edit")
                        return HttpResponseRedirect(
                            reverse("tutor_edit_attendance", kwargs={"attendID": attendanceID}))

        if success:
            messages.success(request, "Successfully edited")
            return HttpResponseRedirect(reverse("tutor_edit_attendance", kwargs={"attendID": attendanceID}))
        else:
            messages.error(request, "Failed to edited")
            return HttpResponseRedirect(reverse("tutor_edit_attendance", kwargs={"attendID": attendanceID}))


# END OF CLASSES SECTION


# SCHEDULES SECTION
def ViewSchedule(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    certified = TutorsCertifiedToCourse.objects.filter(tutor_id=tutor.id)
    course = Course.objects.all()
    schedule = Schedule.objects.filter(tutor_id=tutor.id).order_by('-created_at')
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
                schedule = Schedule(course_id=courseID, duration=duration, day=day, time=time, status=status,
                                    tutor_id=tutor.id)
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


# END OF SCHEDULES SECTION

# COURSE SECTION
def ViewCertCourses(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    certCourse = TutorsCertifiedToCourse.objects.filter(tutor_id=tutor.id).order_by('-created_at')
    course = Course.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(certCourse, 6)

    try:
        certCourses = paginator.page(page)
    except PageNotAnInteger:
        certCourses = paginator.page(1)
    except EmptyPage:
        certCourses = paginator.page(paginator.num_pages)

    context = {"certCourses": certCourses, "course": course}
    return render(request, "Tutor_Pages/view_courses_template.html", context)


def SaveAppliedCourse(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            courseID = request.POST.get("courseID")
            tutor = Tutor.objects.get(super_id=request.user.id)
            certified = TutorsCertifiedToCourse.objects.filter(tutor_id=tutor.id)
            applyForCert = TutorApplyToCertifyToCourse.objects.filter(tutor_id=tutor.id)

            for cert in certified:
                if courseID == str(cert.course_id):
                    return HttpResponse("alreadyCertified")

            for apply in applyForCert:
                if apply.status == "Pending" or apply.status == "Active":
                    return HttpResponse("alreadyApplied")

            try:
                certify = TutorApplyToCertifyToCourse(status="Pending", course_id=courseID, tutor_id=tutor.id)
                certify.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To apply")
            return HttpResponse(reverse("tutor_view_cert_courses"))


# END OF COURSE SECTION


# EARNINGS SECTION
def ViewEarnings(request):
    tutor = Tutor.objects.get(super_id=request.user.id)
    earnings = TutorEarnings.objects.filter(tutor_id=tutor.id).order_by('-created_at')
    allYearsList = []
    yearsList = []

    for earn in earnings:
        year = int(earn.year)
        allYearsList.append(year)

    try:
        earliestYear = min(allYearsList)
        currentDate = datetime.date.today()
        currentYear = currentDate.year
        yearDiff = (currentYear - earliestYear) + 1

        for i in range(yearDiff):
            year = str(earliestYear + i)
            yearsList.append(year)

        yearsList.sort(reverse=True)
    except:
        pass

    page = request.GET.get('page', 1)
    paginator = Paginator(earnings, 6)

    try:
        tutorEarnings = paginator.page(page)
    except PageNotAnInteger:
        tutorEarnings = paginator.page(1)
    except EmptyPage:
        tutorEarnings = paginator.page(paginator.num_pages)

    context = {"yearsList": yearsList, "tutorEarnings": tutorEarnings}
    return render(request, "Tutor_Pages/view_earnings_template.html", context)


# END OF EARNINGS SECTION


# CONTACT US SECTION
def ViewContactUs(request):
    return render(request, "Tutor_Pages/contact_us_template.html")


def SaveContactUs(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax():
            issueTitle = request.POST.get("issueTitle")
            description = request.POST.get("description")
            descriptionFinal = description.replace('\n', '<br>')

            try:
                contactUs = ContactUs(issue_title=issueTitle, description=descriptionFinal, status="Pending",
                                      super_id=request.user.id)
                contactUs.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Failed! To send")
            return HttpResponse(reverse("tutor_contact_us"))


def ViewInquiries(request):
    contactUs = ContactUs.objects.filter(super_id=request.user.id).order_by('-created_at')
    superUser = SuperUser.objects.all()
    admin = Admin.objects.all()
    statusList = []
    statusList.append("Pending")
    statusList.append("Active")
    statusList.append("Closed")
    page = request.GET.get('page', 1)
    paginator = Paginator(contactUs, 6)

    try:
        inquiries = paginator.page(page)
    except PageNotAnInteger:
        inquiries = paginator.page(1)
    except EmptyPage:
        inquiries = paginator.page(paginator.num_pages)

    context = {"inquiries": inquiries, "statusList": statusList, "superUser": superUser, "admin": admin}
    return render(request, "Tutor_Pages/view_inquiries_template.html", context)
# END OF CONTACT US SECTION

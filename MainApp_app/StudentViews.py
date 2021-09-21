import os

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Education_Hub_Management_System.settings import BASE_DIR
from MainApp_app.models import Student, SuperUser, EnrolledStudents, Enrollment, Tutor, Course, EnrollmentDays, \
    EnrollmentTime, AttendancePercent, Attendance, AttendanceStudent, StudentPayment, ContactUs, Admin


# PROFILE SECTION
def ViewProfile(request):
    superUser = SuperUser.objects.get(id=request.user.id)
    student = Student.objects.get(super_id=superUser.id)
    role = "Student"
    context = {"superUser": superUser, "student": student, "role": role}
    return render(request, "Student_Pages/profile_template.html", context)


def SaveProfilePic(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        profilePic = request.FILES['profilePic']
        fs = FileSystemStorage()
        filename = fs.save(profilePic.name, profilePic)
        profilePicUrl = fs.url(filename)

        try:
            student = Student.objects.get(super_id=request.user.id)
            student.pic = profilePicUrl
            student.save()
            messages.success(request, "Uploaded")
            return HttpResponseRedirect(reverse("student_view_profile"))
        except:
            messages.error(request, "Failed to Upload")
            return HttpResponseRedirect(reverse("student_view_profile"))


def RemoveProfilePic(request):
    student = Student.objects.get(super_id=request.user.id)

    if student.pic is not None or student.pic != "":
        if os.path.exists(str(BASE_DIR) + "" + str(student.pic)):
            try:
                os.remove(str(BASE_DIR) + "" + str(student.pic))
                student.pic = ""
                student.save()
                messages.success(request, "Removed")
                return HttpResponseRedirect(reverse("student_view_profile"))
            except:
                messages.error(request, "Failed to Remove")
                return HttpResponseRedirect(reverse("student_view_profile"))

    messages.error(request, "Failed to Remove")
    return HttpResponseRedirect(reverse("student_view_profile"))


def EditProfile(request):
    student = Student.objects.get(super_id=request.user.id)
    context = {"student": student}
    return render(request, "Student_Pages/edit_profile_template.html", context)


def SaveEditProfile(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax:
            currentUsername = request.POST.get("currentUsername")
            currentEmail = request.POST.get("currentEmail")
            username = request.POST.get("username")
            email = request.POST.get("email")
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            gender = request.POST.get("gender")
            dob = request.POST.get("dob")
            phoneNo = request.POST.get("phoneNo")
            superUser = SuperUser.objects.all()

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
                student = Student.objects.get(super_id=request.user.id)
                superUser.username = username
                superUser.email = email
                superUser.first_name = firstName
                superUser.last_name = lastName
                superUser.save()
                student.gender = gender
                student.dob = dob
                student.phone_no = phoneNo
                student.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")

        else:
            messages.error(request, "Failed!")
            return HttpResponseRedirect(reverse("tutor_edit_profile"))
# END OF PROFILE SECTION


# DASHBOARD SECTION
def ViewDashboard(request):
    student = Student.objects.get(super_id=request.user.id)
    enrollmentStudents = EnrolledStudents.objects.filter(student_id=student.id)
    enrollment = Enrollment.objects.all()
    totalActiveClasses = 0
    for enrollStud in enrollmentStudents:
        for enroll in enrollment:
            if enrollStud.enrollment_id == enroll.id:
                if enroll.status == "Active":
                    totalActiveClasses = totalActiveClasses+1

    presentAttendCount = AttendanceStudent.objects.filter(student_id=student.id, status="Present").count()
    absentAttendCount = AttendanceStudent.objects.filter(student_id=student.id, status="Absent").count()
    outstanding = 0
    paid = 0
    payment = StudentPayment.objects.filter(student_id=student.id)

    for pay in payment:
        outstanding = outstanding+float(pay.outstanding)
        paid = paid+float(pay.paid)

    context = {"totalActiveClasses": totalActiveClasses, "presentAttendCount": presentAttendCount,
               "absentAttendCount": absentAttendCount, "outstanding": outstanding, "paid": paid}
    return render(request, "Student_Pages/view_dashboard_template.html", context)
# END OF DASHBOARD SECTION


# TUTOR SECTION
def ViewTutors(request):
    student = Student.objects.get(super_id=request.user.id)
    enrollStudents = EnrolledStudents.objects.filter(student_id=student.id)
    enrollment = Enrollment.objects.all()
    tutor = Tutor.objects.all()
    superUser = SuperUser.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(enrollStudents, 6)

    try:
        enrollStuds = paginator.page(page)
    except PageNotAnInteger:
        enrollStuds = paginator.page(1)
    except EmptyPage:
        enrollStuds = paginator.page(paginator.num_pages)

    context = {"enrollStuds": enrollStuds, "enrollment": enrollment, "tutor": tutor, "superUser": superUser}

    return render(request, "Student_Pages/view_tutors_template.html", context)
# END OF TUTOR SECTION


# CLASSES SECTION
def ViewClasses(request):
    student = Student.objects.get(super_id=request.user.id)
    enrollmentStuds = EnrolledStudents.objects.filter(student_id=student.id).order_by('-created_at')
    enrollment = Enrollment.objects.all()
    enrollmentDays = EnrollmentDays.objects.all()
    enrollmentTime = EnrollmentTime.objects.all()
    tutor = Tutor.objects.all()
    superUser = SuperUser.objects.all()
    course = Course.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(enrollmentStuds, 6)

    try:
        enrollStuds = paginator.page(page)
    except PageNotAnInteger:
        enrollStuds = paginator.page(1)
    except EmptyPage:
        enrollStuds = paginator.page(paginator.num_pages)

    context = {"enrollStuds": enrollStuds, "enrollment": enrollment, "enrollmentDays": enrollmentDays,
               "enrollmentTime": enrollmentTime, "tutor": tutor, "superUser": superUser, "course": course}
    return render(request, "Student_Pages/view_classes_template.html", context)
# END OF CLASSES SECTION


# ATTENDANCE SECTION
def ViewAttendance(request):
    student = Student.objects.get(super_id=request.user.id)
    studentAttendance = AttendancePercent.objects.filter(student_id=student.id)
    enrollment = Enrollment.objects.all()
    course = Course.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(studentAttendance, 6)

    try:
        studentAttend = paginator.page(page)
    except PageNotAnInteger:
        studentAttend = paginator.page(1)
    except EmptyPage:
        studentAttend = paginator.page(paginator.num_pages)
    context = {"studentAttend": studentAttend, "enrollment": enrollment, "course": course}

    return render(request, "Student_Pages/view_attendance_template.html", context)


def ViewAttendanceDetails(request, enrollID):
    student = Student.objects.get(super_id=request.user.id)
    attendance = Attendance.objects.filter(enrollment_id=enrollID)
    attendanceStudent = AttendanceStudent.objects.filter(student_id=student.id).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(attendanceStudent, 6)

    try:
        attendanceStud = paginator.page(page)
    except PageNotAnInteger:
        attendanceStud = paginator.page(1)
    except EmptyPage:
        attendanceStud = paginator.page(paginator.num_pages)

    context = {"attendanceStud": attendanceStud, "attendance": attendance, "id": enrollID}
    return render(request, "Student_Pages/view_attendance_details_template.html", context)
# END OF ATTENDANCE SECTION


# PAYMENT SECTION
def ViewPayment(request):
    student = Student.objects.get(super_id=request.user.id)
    payment = StudentPayment.objects.filter(student_id=student.id, status="Outstanding").order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(payment, 6)

    try:
        pay = paginator.page(page)
    except PageNotAnInteger:
        pay = paginator.page(1)
    except EmptyPage:
        pay = paginator.page(paginator.num_pages)

    context = {"pay": pay}
    return render(request, "Student_Pages/view_payment.html", context)


def SavePayment(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        if request.is_ajax:
            payID = request.POST.get("payID")
            amount = request.POST.get("amount")
            paymentIDCheck = StudentPayment.objects.all()
            existsPayID = False
            status = "Outstanding"

            for payID in paymentIDCheck:
                if payID == str(payID.id):
                    existsPayID = True
                    break

            if not existsPayID:
                return HttpResponse("payID")

            for i in range(len(amount)):
                if amount[i] == "0" or amount[i] == "1" or amount[i] == "2" or amount[i] == "3" or amount[i] == "4" or amount[i] == "5" or amount[i] == "6" or amount[i] == "7" or amount[i] == "8" or amount[i] == "9" or amount[i] == ".":
                    pass
                else:
                    return HttpResponse("amountBadChar")

            payment = StudentPayment.objects.get(id=payID)
            floatAmount = float(amount)
            if floatAmount > float(payment.outstanding):
                return HttpResponse("payingMore")

            if payment.paid is None or payment.paid == "":
                paid = floatAmount
            else:
                paid = float(payment.paid)+floatAmount
            outstanding = float(payment.outstanding)-floatAmount

            if outstanding == 0 or outstanding == 0.0:
                status = "Paid"

            try:
                payment.paid = paid
                payment.outstanding = outstanding
                payment.status = status
                payment.save()
                return HttpResponse("success")
            except:
                return HttpResponse("failed")
        else:
            messages.error(request, "Payment failed")
            return HttpResponseRedirect(reverse("student_view_payment"))
# END OF PAYMENT SECTION


# CONTACT US SECTION
def ViewContactUs(request):
    return render(request, "Student_Pages/contact_us_template.html")


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
            return HttpResponse(reverse("student_view_contact_us"))


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
    return render(request, "Student_Pages/view_inquiries_template.html", context)
# END OF CONTACT US SECTION

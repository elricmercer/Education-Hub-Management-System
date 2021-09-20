"""Education_Hub_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Education_Hub_Management_System import settings
from MainApp_app import views, AdminViews, SuperUserViews, TutorViews, StudentViews

urlpatterns = [
    # COMMON
    path('admin/', admin.site.urls),
    path('', views.ShowLoginPage, name='show_login'),
    path('login', views.DoLogin, name='login'),
    path('logout', views.DoLogout, name='logout'),

    # SUPER USER
    path('admin_view_administrators', SuperUserViews.ViewAdministrators, name="admin_view_administrators"),
    path('admin_add_administrators_save', SuperUserViews.SaveAddAdmin, name="admin_add_administrators_save"),
    path('admin_edit_administrators/<str:superID>', SuperUserViews.EditAdmin, name="admin_edit_administrators"),
    path('admin_edit_administrators_save', SuperUserViews.SaveEditAdmin, name="admin_edit_administrators_save"),
    path('admin_delete_administrators/<str:superUserID>', SuperUserViews.DeleteAdmin, name="admin_delete_administrators"),
    path('admin_view_revenue', SuperUserViews.ViewRevenue, name="admin_view_revenue"),

    # ADMIN
    path('admin_dashboard', AdminViews.Dashboard, name="admin_dashboard"),
    path('admin_profile', AdminViews.Profile, name="admin_profile"),
    path('admin_edit_profile', AdminViews.EditProfile, name="admin_edit_profile"),
    path('admin_edit_profile_save', AdminViews.SaveEditProfile, name="admin_edit_profile_save"),
    path('admin_profile_pic_save', AdminViews.SaveProfilePic, name="admin_profile_pic_save"),
    path('admin_profile_pic_remove', AdminViews.RemoveProfilePic, name="admin_profile_pic_remove"),
    path('admin_view_students', AdminViews.ViewStudents, name="admin_view_students"),
    path('admin_add_students_save', AdminViews.SaveAddStudent, name="admin_add_students_save"),
    path('admin_edit_students/<str:superID>', AdminViews.EditStudent, name="admin_edit_students"),
    path('admin_edit_students_save', AdminViews.SaveEditStudent, name="admin_edit_students_save"),
    path('admin_delete_students/<str:superID>', AdminViews.DeleteStudent, name="admin_delete_students"),
    path('admin_search_student_for_payment', AdminViews.SearchStudentPayment, name="admin_search_student_for_payment"),
    path('admin_view_student_payment/<str:studID>', AdminViews.ViewStudentPayment, name="admin_view_student_payment"),
    path('admin_view_tutors', AdminViews.ViewTutors, name="admin_view_tutors"),
    path('admin_add_tutors_save', AdminViews.SaveAddTutor, name="admin_add_tutors_save"),
    path('admin_delete_tutors/<str:superID>', AdminViews.DeleteTutor, name="admin_delete_tutors"),
    path('admin_edit_tutors/<str:superID>', AdminViews.EditTutor, name="admin_edit_tutors"),
    path('admin_edit_tutors_save', AdminViews.SaveEditTutor, name="admin_edit_tutors_save"),
    path('admin_search_tutor_payment', AdminViews.SearchTutorPayment, name="admin_search_tutor_payment"),
    path('admin_view_tutor_payment/<str:tutorID>', AdminViews.ViewTutorPayment, name="admin_view_tutor_payment"),
    path('admin_view_course', AdminViews.ViewCourse, name="admin_view_course"),
    path('admin_add_course_save', AdminViews.SaveAddCourse, name="admin_add_course_save"),
    path('admin_delete_course/<str:courID>', AdminViews.DeleteCourse, name="admin_delete_course"),
    path('admin_edit_course/<str:courID>', AdminViews.EditCourse, name="admin_edit_course"),
    path('admin_edit_course_save', AdminViews.SaveEditCourse, name="admin_edit_course_save"),
    path('admin_search_tutor_certification', AdminViews.SearchTutorCertification, name="admin_search_tutor_certification"),
    path('admin_view_tutor_certifications/<str:tutID>', AdminViews.ViewTutorCertifications, name="admin_view_tutor_certifications"),
    path('admin_tutor_certification_save', AdminViews.SaveTutorCertification, name="admin_tutor_certification_save"),
    path('admin_delete_tutor_certification/<str:certID>/<str:tutorID>', AdminViews.DeleteTutorCertification, name="admin_delete_tutor_certification"),
    path('admin_view_schedules', AdminViews.ViewSchedules, name="admin_view_schedules"),
    path('admin_schedules_save', AdminViews.SaveAddSchedule, name="admin_schedules_save"),
    path('admin_delete_schedule/<str:schID>', AdminViews.DeleteSchedule, name="admin_delete_schedule"),
    path('admin_add_tutor_to_schedule', AdminViews.SaveAddTutorToSchedule, name="admin_add_tutor_to_schedule"),
    path('admin_edit_schedule/<str:schID>', AdminViews.EditSchedule, name="admin_edit_schedule"),
    path('admin_edit_schedule_save', AdminViews.SaveEditSchedule, name="admin_edit_schedule_save"),
    path('admin_view_classes', AdminViews.ViewClasses, name="admin_view_classes"),
    path('admin_add_classes_save', AdminViews.SaveAddClasses, name="admin_add_classes_save"),
    path('admin_add_students_to_class_save', AdminViews.SaveAddStudentsToClass, name="admin_add_students_to_class_save"),
    path('admin_add_tutor_to_class_save', AdminViews.SaveAddTutorToClass, name="admin_add_tutor_to_class_save"),
    path('admin_remove_student_from_class', AdminViews.RemoveStudentFromClass, name="admin_remove_student_from_class"),
    path('admin_remove_tutor_from_class', AdminViews.RemoveTutorFromClass, name="admin_remove_tutor_from_class"),
    path('admin_add_link_for_class_save', AdminViews.SaveAddClassRoomLink, name="admin_add_link_for_class_save"),
    path('admin_remove_link_for_class', AdminViews.RemoveClassRoomLink, name="admin_remove_link_for_class"),
    path('admin_edit_class/<str:enrollID>', AdminViews.EditClass, name="admin_edit_class"),
    path('admin_delete_class/<str:enrollID>', AdminViews.DeleteClass, name="admin_delete_class"),
    path('admin_edit_class_save', AdminViews.SaveEditClass, name="admin_edit_class_save"),
    path('admin_view_inquiries', AdminViews.ViewInquiries, name="admin_view_inquiries"),
    path('admin_update_inquiry_status_save', AdminViews.UpdateInquiryStatus, name="admin_update_inquiry_status_save"),
    path('admin_view_tutor_certify_request', AdminViews.ViewCertifyRequest, name="admin_view_tutor_certify_request"),
    path('admin_tutor_certify_request_save', AdminViews.SaveCertifyRequest, name="admin_tutor_certify_request_save"),

    # TUTOR
    path('tutor_dashboard', TutorViews.Dashboard, name="tutor_dashboard"),
    path('tutor_profile', TutorViews.Profile, name="tutor_profile"),
    path('tutor_profile_pic_save', TutorViews.SaveProfilePic, name="tutor_profile_pic_save"),
    path('tutor_remove_profile_pic', TutorViews.RemoveProfilePic, name="tutor_remove_profile_pic"),
    path('tutor_edit_profile', TutorViews.EditProfile, name="tutor_edit_profile"),
    path('tutor_edit_profile_save', TutorViews.SaveEditProfile, name="tutor_edit_profile_save"),
    path('tutor_view_students', TutorViews.ViewStudents, name="tutor_view_students"),
    path('tutor_view_classes', TutorViews.ViewClasses, name="tutor_view_classes"),
    path('tutor_view_schedules', TutorViews.ViewSchedule, name="tutor_view_schedules"),
    path('tutor_schedules_save', TutorViews.SaveSchedule, name="tutor_schedules_save"),
    path('tutor_edit_schedule/<str:schID>', TutorViews.EditSchedule, name="tutor_edit_schedule"),
    path('tutor_edit_schedule_save', TutorViews.SaveEditSchedule, name="tutor_edit_schedule_save"),
    path('tutor_delete_schedule/<str:schID>', TutorViews.DeleteSchedule, name="tutor_delete_schedule"),
    path('tutor_view_cert_courses', TutorViews.ViewCertCourses, name="tutor_view_cert_courses"),
    path('tutor_apply_cert_course_save', TutorViews.SaveAppliedCourse, name="tutor_apply_cert_course_save"),
    path('tutor_view_earnings', TutorViews.ViewEarnings, name="tutor_view_earnings"),
    path('tutor_contact_us', TutorViews.ViewContactUs, name="tutor_contact_us"),
    path('tutor_contact_us_save', TutorViews.SaveContactUs, name="tutor_contact_us_save"),
    path('tutor_view_inquiries', TutorViews.ViewInquiries, name="tutor_view_inquiries"),

    # STUDENT
    path('student_view_profile', StudentViews.ViewProfile, name="student_view_profile"),
    path('student_view_dashboard', StudentViews.ViewDashboard, name="student_view_dashboard"),
    path('student_profile_pic_save', StudentViews.SaveProfilePic, name="student_profile_pic_save"),
    path('student_remove_profile_pic', StudentViews.RemoveProfilePic, name="student_remove_profile_pic"),
    path('student_edit_profile', StudentViews.EditProfile, name="student_edit_profile"),
    path('student_edit_profile_save', StudentViews.SaveEditProfile, name="student_edit_profile_save"),
    path('student_view_tutors', StudentViews.ViewTutors, name="student_view_tutors"),
    path('student_view_classes', StudentViews.ViewClasses, name="student_view_classes"),
    path('student_view_attendance', StudentViews.ViewAttendance, name="student_view_attendance"),
    path('student_view_attendance_details/<str:enrollID>', StudentViews.ViewAttendanceDetails, name="student_view_attendance_details"),
    path('student_view_payment', StudentViews.ViewPayment, name="student_view_payment"),
    path('student_payment_save', StudentViews.SavePayment, name="student_payment_save"),
    path('student_view_contact_us', StudentViews.ViewContactUs, name="student_view_contact_us"),
    path('student_contact_us_save', StudentViews.SaveContactUs, name="student_contact_us_save"),
    path('student_view_inquiries', StudentViews.ViewInquiries, name="student_view_inquiries"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

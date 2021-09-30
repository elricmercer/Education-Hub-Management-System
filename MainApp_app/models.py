from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SuperUser(AbstractUser):
    user_type_data = ((1, "SuperUser"), (2, "Admin"), (3, "Tutor"), (4, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=20)


class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    super = models.OneToOneField(SuperUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=20)
    pic = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Tutor(models.Model):
    id = models.BigAutoField(primary_key=True)
    super = models.OneToOneField(SuperUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=20)
    pic = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    super = models.OneToOneField(SuperUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=20)
    pic = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    info = models.TextField(blank=True, null=True)
    outstanding = models.CharField(max_length=255, blank=True, null=True)
    paid = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.CharField(max_length=20)
    day = models.CharField(max_length=15)
    time = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Enrollment(models.Model):
    id = models.BigAutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.CharField(max_length=15)
    end_date = models.CharField(max_length=15)
    status = models.CharField(max_length=10)
    link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class EnrollmentDays(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    monday = models.CharField(max_length=5, blank=True, null=True)
    tuesday = models.CharField(max_length=5, blank=True, null=True)
    wednesday = models.CharField(max_length=5, blank=True, null=True)
    thursday = models.CharField(max_length=5, blank=True, null=True)
    friday = models.CharField(max_length=5, blank=True, null=True)
    saturday = models.CharField(max_length=5, blank=True, null=True)
    sunday = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class EnrollmentTime(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    monday = models.CharField(max_length=10, blank=True, null=True)
    tuesday = models.CharField(max_length=10, blank=True, null=True)
    wednesday = models.CharField(max_length=10, blank=True, null=True)
    thursday = models.CharField(max_length=10, blank=True, null=True)
    friday = models.CharField(max_length=10, blank=True, null=True)
    saturday = models.CharField(max_length=10, blank=True, null=True)
    sunday = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class EnrolledStudents(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    start_time = models.CharField(max_length=10)
    duration = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceStudent(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendancePercent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    percent = models.CharField(max_length=8, null=True, blank=True)
    represent = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TutorsCertifiedToCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TutorApplyToCertifyToCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TutorEarnings(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    earned = models.CharField(max_length=255)
    month = models.CharField(max_length=5)
    year = models.CharField(max_length=6)
    info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class CompanyEarnings(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_payment = models.ForeignKey(StudentPayment, on_delete=models.CASCADE)
    earned = models.CharField(max_length=255)
    month = models.CharField(max_length=5)
    year = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class ContactUs(models.Model):
    id = models.BigAutoField(primary_key=True)
    issue_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    super = models.OneToOneField(SuperUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=SuperUser)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(super=instance)
        if instance.user_type == 2:
            Admin.objects.create(super=instance)
        if instance.user_type == 3:
            Tutor.objects.create(super=instance)
        if instance.user_type == 4:
            Student.objects.create(super=instance)


@receiver(post_save, sender=SuperUser)
def saveUserProfile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.admin.save()
    if instance.user_type == 3:
        instance.tutor.save()
    if instance.user_type == 4:
        instance.student.save()

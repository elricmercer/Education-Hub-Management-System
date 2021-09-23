from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "MainApp_app.AdminViews":
                    pass
                elif modulename == "MainApp_app.views":
                    pass
                elif modulename == "MainApp_app.SuperUserViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "2":
                if modulename == "MainApp_app.AdminViews":
                    pass
                elif modulename == "MainApp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "3":
                if modulename == "MainApp_app.TutorViews":
                    pass
                elif modulename == "MainApp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("tutor_dashboard"))
            elif user.user_type == "4":
                if modulename == "MainApp_app.StudentViews":
                    pass
                elif modulename == "MainApp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_view_dashboard"))
            else:
                return HttpResponseRedirect(reverse("show_login"))
        else:
            if request.path == reverse("show_login") or request.path == reverse(
                    "doLogin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))

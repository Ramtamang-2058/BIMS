from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__modulle__
        user = request.user  # who is current user ?
        if user.is_authencticated:
            if user.role == 1:
                if modulename == 'hospital_admin.views':
                    error = True
                    if request.path == reverse('hospitalDetailView'):
                        pass
                    else:
                        messages.error(request, "You do not have access to this resource")
                        return redirect(reverse("hospitalDetailView"))

            elif user.role == 3:
                if modulename == 'administrator.views':
                    messages.error(request, "You do not have this access.")
                    return redirect(reverse('adminDashboard'))

            elif user.role == 4:
                if modulename == 'trainer.views':
                    pass
                else:
                    messages.error(request, "you donot have access to this resource.")
                    return redirect(reverse('trainerDashboard'))

            else:
                if request.path == reverse('account_login'):
                    pass
                elif modulename == 'administrator.views':
                    messages.error(request, "You need to be logged in to perform this operation.")
                    return redirect(reverse('account_login'))
                else:
                    return redirect(reverse('account_login'))

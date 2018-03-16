from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.apps.usercabinet.forms import ProfileSettingsForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, View, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from psmate.models import Enterprises


# class RegisterFormView(FormView):
#     form_class = UserRegisterForm
#     template_name = "regform.html"
#     success_url = "/settings/"
#
#     def form_valid(self, form):
#         # create user
#         form.save()
#         # get email-password
#         email = self.request.POST['email']
#         password = self.request.POST['password1']
#         #authenticate user then login
#         user = authenticate(username=email, password=password)
#         login(self.request, user)
#
#         # call base class method
#         return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "layouts/layout.html"

    success_url = "/cabinet/"

    def form_valid(self, form):
        # Get user object
        self.user = form.get_user()

        # Auth user
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)



class LogoutView(View):
    def get(self, request):

        logout(request)

        # redirect to  index.html after logout
        return HttpResponseRedirect("/")



class UserCabinetView(View):
    form_class = ProfileSettingsForm
    template_name = 'usercabinet/index.html'
    model = User

    def get(self, request, *args, **kwargs):

        user = self.request.user
        companies = Enterprises.objects.filter(regname_id=user.id)

        return render(request, self.template_name, {'user': user,
                                                    'companies' :companies,

                                                        })


class UserSettingsView(UpdateView):
    form_class = ProfileSettingsForm
    template_name = 'usercabinet/settings.html'
    model = User
    success_url = "/cabinet/"

    def dispatch(self, *args, **kwargs):
        return super(UserSettingsView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):

        user = self.request.user

        return user


    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super(UserSettingsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()


        return super(UserSettingsView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cabinet')

    def get_form_kwargs(self):
        kwargs = super(UserSettingsView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user

        return kwargs


    def form_valid(self, form):
        self.object = self.get_object()
        return super(UserSettingsView, self).form_valid(form)

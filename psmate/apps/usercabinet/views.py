from django.shortcuts import render

from django.views.generic.edit import FormView

from psmate.apps.usercabinet.forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout


class RegisterFormView(FormView):
    form_class = UserRegisterForm

    # enter to cabinet
    success_url = "/cabinet/"

    template_name = "regform.html"

    def form_valid(self, form):
        # create user
        form.save()
        # get email-password
        email = self.request.POST['email']
        password = self.request.POST['password1']
        #authenticate user then login
        user = authenticate(username=email, password=password)
        login(self.request, user)

        # call base class method
        return super(RegisterFormView, self).form_valid(form)
    
  
class LoginFormView(FormView):
    form_class = AuthenticationForm
   
    template_name = "loginform.html"
    
    success_url = "/"

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

  
  
    
def usercabinet(request):
    return render(request, 'usercabinet/index.html')

def settings(request):
    return render(request, 'usercabinet/settings.html')



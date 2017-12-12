from django.shortcuts import render

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth import login


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # enter to cabinet
    success_url = "/cabinet/"

    template_name = "regform.html"

    def form_valid(self, form):
        # create user
        form.save()

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



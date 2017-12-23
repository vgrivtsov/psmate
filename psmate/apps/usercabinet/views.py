from django.shortcuts import render

from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.apps.usercabinet.forms import UserRegisterForm
from psmate.apps.usercabinet.forms import ProfileSettingsForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

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

#  
# class SettingsFormView(UpdateView):
#     form_class = ProfileSettingsForm
#     template_name = "usercabinet/settings.html"
#     
#     success_url = "/settings/"  # You should be using reverse here
# 
#     def get_object(self):
#         return User.objects.get(email=self.request.user)
#

@login_required    
def usercabinet(request):
    
    if request.method == 'POST':
        
        # get current user to form - see ProfileSettingsForm __init__
        form = ProfileSettingsForm(request.user, request.POST, instance=request.user)
        

        if form.is_valid():

            form.save()
            context = {'form': form}

            return render(request, 'usercabinet/index.html', context)

        
    else:
        form = ProfileSettingsForm(request.user, instance=request.user)

    return render(request, 'usercabinet/index.html', {'form': form})




# def settings(request):
#     return render(request, 'usercabinet/settings.html')

@login_required
def settings(request):
    
    if request.method == 'POST':
        
        # get current user to form - see ProfileSettingsForm __init__
        form = ProfileSettingsForm(request.user, request.POST, instance=request.user)
        

        if form.is_valid():

            form.save()
            context = {'form': form}

            return render(request, 'usercabinet/settings.html', context)

        
    else:
        form = ProfileSettingsForm(request.user, instance=request.user)

    return render(request, 'usercabinet/settings.html', {'form': form})


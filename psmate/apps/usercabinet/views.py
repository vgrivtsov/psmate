from django.shortcuts import render

from django.views.generic.edit import FormView

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

 
# class SettingsFormView(UpdateView):
#     model = User 
#    
#     form_class = ProfileSettingsForm
#    
#     template_name = "usercabinet/settings.html"
#     
#     success_url = "/cabinet/"
# 
# 
#     def get_object(self, request):
#            form = PasswordChangeForm(user=request.user, data=request.POST)
#            if form.is_valid():
#                form.save()
#                update_session_auth_hash(request, form.user)
#         return self.request.user


    # def form_valid(self, form):
    #     # Get user object
    #     self.user = get_object()
    #     form.save(commit=False)
    # 
    #     return super(SettingsFormView, self).form_valid(form)  
    # 
  
    
def usercabinet(request):
    return render(request, 'usercabinet/index.html')




# def settings(request):
#     return render(request, 'usercabinet/settings.html')

@login_required
def settings(request):
    
    if request.method == 'POST':
        
        form = ProfileSettingsForm(request.POST, instance=request.user)
        #update = form.save(commit=False)
       # update.user = request.user
        if form.is_valid:
           
            form.save()       
        
        
    else:
        form = ProfileSettingsForm(instance=request.user)

    return render(request, 'usercabinet/settings.html', {'form': form})



# def home(request):
#     user = request.user # or ...
#     if request.POST:
#         userform = UserForm(request.POST, instance=user)
#         profileform = ProfileForm(request.POST, instance=user.get_profile())
#         if userform.is_valid() and profileform.is_valid():
#             # save
#     else:
#         userform = UserForm(instance=user)
#         profileform = ProfileForm(instance=user.get_profile())
#     return render_to_response('home.html', {
#         'userform': userform,
#         'profileform': profileform
#     })        




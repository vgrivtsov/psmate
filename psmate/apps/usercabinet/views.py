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
from django.views.generic import FormView, ListView, View, UpdateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages


from psmate.models import Enterprises, Orders
from datetime import datetime, timedelta

from braces.views import FormMessagesMixin
from envelope.views import ContactView

from django.utils.translation import ugettext_lazy as _

from .forms import MyContactForm

from django_robokassa.forms import RobokassaForm
from django.shortcuts import get_object_or_404, render

from datetime import datetime, timedelta

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
        paidactivdate = request.user.profiles.paidactivdate
        companies = Enterprises.objects.filter(regname_id=user.id)

        stop_paidactivdate = True

        if paidactivdate:
            #paidactivdate = datetime.strptime( paidactivdate, "%Y-%m-%d" )
            datenow = datetime.now().date()

            # m= timedelta(days=31)
            # m3 = timedelta(days=93)
            # y = timedelta(days=366)
            #print(m, m3, y)

            if (paidactivdate - datenow).days + 1 > 0:
                stop_paidactivdate = False


            # if (paidactivdate - datenow).days + 1 > 0:
            #     balance = paidactivdate - datenow
            # else:
            #     balance = timedelta(0)

            # print('balance', balance)
            # new_paidactivdate = datenow + m + balance
            # print(new_paidactivdate)



        return render(request, self.template_name, {'user': user,
                                                    'companies' :companies,
                                                    'stop_paidactivdate' :stop_paidactivdate
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


class PricingView(TemplateView):

    template_name = 'pricing.html'
    model = User

    def get(self, request, *args, **kwargs):

       # user = self.request.user

        return render(request, self.template_name)


class MyContactView(FormMessagesMixin, ContactView):
    form_invalid_message = _(u"There was an error in the contact form.")
    form_valid_message = _(u"Thank you for your message.")
    form_class = MyContactForm


# class MakeOrder(View):
#
#     success_url = "/purchase/"
#     model = Orders
#
#     def get_context_data(self, request, *args, **kwargs):
#
#         user = self.request.user
#         purchase_name = self.kwargs['purchase_name']
#
#         if purchase_name == '1month':
#             name = 'Оплата за 1 месяц использования сервиса ПрофНавигатор'
#             out_summ = 600
#
#         elif purchase_name == '3month':
#             name = 'Оплата за 3 месяца использования сервиса ПрофНавигатор'
#             out_summ = 1500
#
#         elif purchase_name == '12month':
#             name = 'Оплата за год использования сервиса ПрофНавигатор'
#             out_summ = 4800
#
#         else:
#             messages.error(request, "Ошибка - неверная сумма")
#             return reverse_lazy('pricing')
#
#
#         order = Orders.objects.create(user_id=user.id, name=name, out_summ=out_summ)
#
#         return super(MakeOrder, self).get_context_data(**kwargs)



class RobokassaView(FormView):

    template_name = 'robokassa/pay_with_robokassa.html'
    form_class = RobokassaForm
    models= Orders

    def dispatch(self, *args, **kwargs):
        return super(RobokassaView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        user = self.request.user

        purchase_name = self.kwargs['purchase_name']
        print(user, purchase_name)

        if purchase_name == '600':
            order_name = 'Оплата за 1 месяц использования сервиса ПрофНавигатор'
            out_summ = 560.75
            period = '3 месяца'
            commission = 600- 560.75

        elif purchase_name == '1500':
            order_name = 'Оплата за 3 месяца использования сервиса ПрофНавигатор'
            out_summ = 1401.87
            period = '1 месяц'
            commission = 1500- 1401.87

        elif purchase_name == '4800':
            order_name = 'Оплата за год использования сервиса ПрофНавигатор'
            out_summ = 4485.98
            period = '1 год'
            commission = 4800 - 4485.98

        else:
            messages.error(request, "Ошибка - неверная сумма")
            return reverse_lazy('pricing')


        order = Orders.objects.create(user_id=user.id, name=order_name, out_summ=out_summ, created_at=datetime.now())

        #print(purchase_name, order.id, out_summ, user.email, datetime.now().date())


        generaldata = { 'purchase_name' : purchase_name,
                       'ordernum' : order.id,
                       'period' : period,
                       'commission' : commission,
                       'out_summ' : out_summ,

                       }

        form = RobokassaForm(initial={
                   'IncCurrLabel' : 'BankCard',
                   'OutSum': out_summ,
                   'InvId': order.id,
                   'Desc': order_name,
                   'Email': user.email,
                   # 'IncCurrLabel': '',
                   # 'Culture': 'ru'
               })

        return render(request, self.template_name, {'form': form, 'generaldata' : generaldata})


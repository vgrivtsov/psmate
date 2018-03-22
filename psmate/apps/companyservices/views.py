from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import FormView, ListView, View, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.models import Enterprises, Departs, Jobtitles
from psmate.apps.services.views import ShowJTlist, JTDetailsView, OfficialInstructions

from psmate.apps.companyservices.forms import OrgCreateForm, OrgUpdateForm
from psmate.apps.companyservices.forms import DepartCreateForm, DepartUpdateForm
from psmate.apps.companyservices.forms import OICreateForm
from django.http import Http404
from django.contrib import messages

from psmate.models import *

from datetime import datetime, timedelta
from operator import itemgetter
import pymorphy2
from pymorphy2 import units
import pytils
import re
import docxtpl
import locale
import pymorphy2
import io


################ ORGANIZATIONS VIEWS ###################################################

class OrgCreateView(FormView):
    form_class = OrgCreateForm
    template_name = "companyservices/regform.html"
    success_url = "/cabinet/"

    def get_form_kwargs(self):
        kwargs = super(OrgCreateView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user

        return kwargs

    def form_valid(self, form):

        # create company
        form.save()

        e_name = self.request.POST['e_name']
        e_op_form = self.request.POST['e_op_form']
        e_director = self.request.POST['e_director']
        e_fam_ul = self.request.POST['e_fam_ul']
        e_name_ul = self.request.POST['e_name_ul']
        e_otch_ul = self.request.POST['e_otch_ul']
        regname_id = self.request.user.id

        # call base class method
        return super(OrgCreateView, self).form_valid(form)



class OrgReadView(View):

    template_name = 'companyservices/organization-profile.html'
    model = User


    def get(self, request, *args, **kwargs):

        user = self.request.user
        paidactivdate = request.user.profiles.paidactivdate
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

        company_id = self.kwargs['id']

        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            company = Enterprises.objects.get(pk=company_id)
            departs = Departs.objects.filter(company_id=company_id)
            ois = Offinsts.objects.filter(company_id=company_id)

            for oi in ois:

                oi.short = oi.name[:30]+'...' # truncate long JT name
                if oi.tfs:
                    tfsnew = oi.tfs.split(",")
                    oi.tfs = [int(x) for x in tfsnew]



        return render(request, self.template_name, {'company' : company,
                                                    'departs' :departs,
                                                    'ois' :ois,
                                                    'stop_paidactivdate' :stop_paidactivdate
                                                    })


class OrgUpdateView(UpdateView):
    form_class = OrgUpdateForm
    template_name = 'companyservices/settings.html'
    model = Enterprises


    def get_object(self, queryset=None):

        obj = Enterprises.objects.get(id=self.kwargs['id'])
        return obj


    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super(OrgUpdateView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        self.object = self.get_object()


        return super(OrgUpdateView, self).post(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})


    def get_form_kwargs(self):

        kwargs = super(OrgUpdateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user

        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user


        return kwargs


    def form_valid(self, form):

        self.object = self.get_object()
        return super(OrgUpdateView, self).form_valid(form)



class OrgDeleteView(DeleteView):

    template_name = "companyservices/enterprises_confirm_delete.html"
    success_url = "/cabinet/"


    def get_object(self, queryset=None):

        obj = Enterprises.objects.get(pk=self.kwargs['id'])
        return obj


    def get(self, request, *args, **kwargs):

        user = self.request.user
        company_id = self.kwargs['id']

        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            company = Enterprises.objects.get(pk=company_id)

        return render(request, self.template_name, {'company' : company})


    def get_queryset(self):

        user = self.request.user
        company_id =  self.kwargs['id']


        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            return Enterprises.objects.get(pk=company_id)


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "Организация %s была удалена" % obj.e_name)
        return super(OrgDeleteView, self).delete(request, *args, **kwargs)


################ DEPARTS VIEWS ###################################################


class DepartCreateView(FormView):
    form_class = DepartCreateForm
    template_name = "companyservices/departregform.html"


    def get_form_kwargs(self):

        kwargs = super(DepartCreateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user

        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user


        return kwargs


    def form_valid(self, form):

        # create company
        form.save()

        name = self.request.POST['name']
        cheef = self.request.POST['cheef']
        cheef_fam = self.request.POST['cheef_fam']
        cheef_name = self.request.POST['cheef_name']
        cheef_otch = self.request.POST['cheef_otch']
        phone = self.request.POST['phone']
        #company_id = self.company_id

        # call base class method
        return super(DepartCreateView, self).form_valid(form)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})


class DepartUpdateView(UpdateView):

    form_class = DepartUpdateForm
    template_name = 'companyservices/departsettings.html'
    model = Departs


    def get_object(self, queryset=None):

        obj = Departs.objects.get(id=self.kwargs['pk'])
        return obj


    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super(DepartUpdateView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        self.object = self.get_object()


        return super(DepartUpdateView, self).post(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})


    def get_form_kwargs(self):

        kwargs = super(DepartUpdateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user

        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user


        return kwargs


    def form_valid(self, form):
        self.object = self.get_object()
        return super(DepartUpdateView, self).form_valid(form)


class DepartDeleteView(DeleteView):

    template_name = "companyservices/departs_confirm_delete.html"


    def get(self, request, *args, **kwargs):

        user = self.request.user
        company_id = self.kwargs['id']
        dep_id =  self.kwargs['pk']

        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            company = Enterprises.objects.get(pk=company_id)
            department = Departs.objects.filter(id=dep_id)[0]

        return render(request, self.template_name, {'company' : company, 'department' : department })


    def get_queryset(self):

        user = self.request.user
        company_id =  self.kwargs['id']
        dep_id =  self.kwargs['pk']

        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            return Departs.objects.filter(id=dep_id)


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "Подразделение %s было удалено" % obj.name)
        return super(DepartDeleteView, self).delete(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})

################### OFFICIAL INSTRUCTIONS VIEW ########################3


class OIsearchJTView(ShowJTlist): # overriding ShowJTlist from psmate.apps.services.views

    template_name = "companyservices/jobtitles-list.html"

    def get_context_data(self, **kwargs):
        context = super(OIsearchJTView, self).get_context_data(**kwargs)

        companyid = self.kwargs['id']
        departid = self.kwargs['pk']
        company = Enterprises.objects.get(id=companyid)
        department = Departs.objects.get(id=departid)
        context['cmpd'] =  {'company' : company, 'department' : department}

        return context


class OIJTDetailsView(JTDetailsView):

    template_name = "companyservices/jobtitle-details.html"
    model = Jobtitles

    def get(self, request, *args, **kwargs):

        jt_slug =  self.kwargs['slug']

        companyid = self.kwargs['id']
        departid = self.kwargs['pk']
        company = Enterprises.objects.get(id=companyid)
        department = Departs.objects.get(id=departid)

        cmpd = {'company' : company, 'department' : department}

        if jt_slug:

            jt = Jobtitles.objects.filter(slug=jt_slug)

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id)
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id)
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id)
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id)
            tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
            gtf = Gtfinfo.objects.get(id=jt[0].gtf_id)

            otrasl = ps[0].otraslid

            jtresult = {'id' : jt[0].id,
                        'slug' : jt[0].slug,
                        'jobtitle' : jt[0].jobtitle,
                        'levelofquali' : gtf.levelofquali,
                        'codeotf' : gtf.codeotf,
                        'nameotf' : jt[0].nameotf,
                        'pspurposekind' : ps[0].pspurposekind,
                        'nameps' : ps[0].nameps,
                        'psregnum' : ps[0].psregnum,
                        'psid' : ps[0].id,
                        'otraslname' : otrasl.name,
                        'otraslicon' : otrasl.icon,
                        'educationalreqs' : educationalreqs,
                        'reqworkexperiences' : reqworkexperiences,
                        'specialconditions' : specialconditions,
                        'othercharacts' : othercharacts,
                        'tfs' : tfs,

                        }

            return render(request, self.template_name, {'jtresult': jtresult, 'cmpd': cmpd })


class OICreateView(ListView):

    template_name = "companyservices/official-instructions-new.html"
    model = Jobtitles

    def get(self, request,  *args, **kwargs):

        data =  self.kwargs['slug']
        docx =  self.kwargs['docx']
        tfsid = [int(x) for x in self.request.GET.getlist('tfids')]
        companyid = self.kwargs['id']
        departid = self.kwargs['pk']
        company = Enterprises.objects.get(id=companyid)
        department = Departs.objects.get(id=departid)

        ois = Offinsts.objects.filter(departs_id=departid)
        ois_len = len(ois)
        user = self.request.user
        paidactivdate = request.user.profiles.paidactivdate

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


        cmpd0 = {'company' : company, 'department' : department}

        if data != None:

            morph = pymorphy2.MorphAnalyzer()
            pos_list = ['NOUN', 'ADJF', 'ADJS', 'PRTF', 'PRTS']  # Chast' rechi & padezh

            jt = Jobtitles.objects.filter(slug=data)

            ######### company-department data #######################################

            company = Enterprises.objects.get(id=companyid)
            department = Departs.objects.get(id=departid)

            e_name = company.e_name
            e_op_form = company.e_op_form
            e_director = company.e_director
            e_fam_ul = company.e_fam_ul
            e_name_ul = company.e_name_ul
            e_otch_ul = company.e_otch_ul

            depname = department.name
            cheef = department.cheef
            cheef_name = department.cheef_name
            cheef_otch = department.cheef_otch
            cheef_fam = department.cheef_fam

            ### roditelny, datelny padezhi ###

            # CEO to padezhi
            director_gent = []
            director_datv = []

            for w in e_director.split(' '): # split CEO pozition
                capmarker = False
                if not w.islower() and not w.isupper(): # check if word is capitalized
                    capmarker = True

                cleared_director = morph.parse(w)[0]

                if cleared_director.tag.POS in pos_list and cleared_director.tag.case == 'nomn' and cleared_director.tag.number == 'sing': # check if word is single noun

                    e_dir_gent = cleared_director.inflect({'gent'}).word
                    e_dir_datv = cleared_director.inflect({'datv'}).word

                    director_gent.append(e_dir_gent.capitalize() if capmarker == True else e_dir_gent )
                    director_datv.append(e_dir_datv.capitalize() if capmarker == True else e_dir_datv)
                else:
                    director_gent.append(w.capitalize() if capmarker == True else w)
                    director_datv.append(w.capitalize() if capmarker == True else w)


            e_director_gent = ' '.join(director_gent)
            e_director_datv = ' '.join(director_datv)

            # Cheef to padezhi
            cheef_datv = []

            for w in cheef.split(' '): # split CEO pozition
                capmarker = False
                if not w.islower() and not w.isupper(): # check if word is capitalized
                    capmarker = True

                cleared_cheef = morph.parse(w)[0]
                print(cleared_cheef)

                if cleared_cheef.tag.POS in pos_list and cleared_cheef.tag.case == 'nomn' and cleared_cheef.tag.number == 'sing': # check if word is single noun
                    d_cheef_datv = cleared_cheef.inflect({'datv'}).word

                    cheef_datv.append(d_cheef_datv.capitalize() if capmarker == True else d_cheef_datv)
                else:
                    cheef_datv.append(w.capitalize() if capmarker == True else w)


            d_cheef_datv = ' '.join(cheef_datv)

            cmpd = {  'e_name' : e_name,
                      'e_op_form' : e_op_form,
                      'e_director' : e_director,
                      'e_fam_ul' : e_fam_ul,
                      'e_name_ul' : e_name_ul,
                      'e_otch_ul' : e_otch_ul,
                      'e_director_gent' : e_director_gent,
                      'e_director_datv' : e_director_datv,
                      'depname' : depname,
                      'cheef' : cheef,
                      'cheef_name' : cheef_name,
                      'cheef_otch' : cheef_otch,
                      'cheef_fam' : cheef_fam,
                      'd_cheef_datv' : d_cheef_datv
                    }

            ##### nowdate in roditelny padezh(need for docx generation)##

            m = pymorphy2.MorphAnalyzer()
            locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
            today = datetime.now().strftime("%d %B %Y").lower()

            today, month, year = today.split(' ')
            nmonth = m.parse(month)[0].inflect({'gent'}).word


            ######### general data #######################################

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id).distinct()
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id).distinct()
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id).distinct()
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id).distinct()
            #tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
            otrasl = ps[0].otraslid

            generaldatas = []

            #make jobtitle Roditelny padezh

            jt_rod = []

            #cut non need padezh string beetween '( )'
            pattern = re.compile("[\(\[].*?[\)\]]")
            if re.findall(pattern, jt[0].jobtitle):
                cuttedstring = re.findall(pattern, jt[0].jobtitle)[0]
            else:
                cuttedstring = ''

            cleared_jt = re.sub("[\(\[].*?[\)\]]", "", jt[0].jobtitle)

            for i in cleared_jt.split(' '):
                p = morph.parse(i)[0]
                if p.tag.POS in pos_list and p.tag.case == 'nomn': # Chast' rechi & padezh

                    if p.inflect({'gent'}) :

                        changed_word = p.inflect({'sing', 'gent'}).word
                        if changed_word == 'риска-менеджера':
                            changed_word = 'риск-менеджера'
                        if changed_word == 'бренда-менеджера':
                            changed_word = 'бренд-менеджера'
                        if changed_word == 'брэнда-менеджера':
                            changed_word = 'брэнд-менеджера'
                        if changed_word == 'чокерноя':
                            changed_word = 'чокерной'

                        jt_rod.append(changed_word)
                    else:

                        jt_rod.append(i)
                else:
                    jt_rod.append(i)

            jobtitlerod = ' '.join(jt_rod) + ' '+cuttedstring

            generaldatas = {
                    'slug' : data,
                    'jobtitleid' : jt[0].id,
                    'jobtitle' : jt[0].jobtitle,
                    'jobtitlerod' : jobtitlerod,
                    'nameotf' : jt[0].nameotf,
                    'pspurposekind' : ps[0].pspurposekind,
                    'nameps' : ps[0].nameps,
                    'psregnum' : ps[0].psregnum,
                    'psordernum' : ps[0].psordernum,
                    'psdateappr' : ps[0].psdateappr,
                    'otraslname' : otrasl.name,
                    'otraslicon' : otrasl.icon,
                    'educationalreqs' : educationalreqs,
                    'reqworkexperiences' : reqworkexperiences,
                    'specialconditions' : specialconditions,
                    'othercharacts' : othercharacts,
                    'today' : today,
                    'month': nmonth,
                    'year' :year
                    }

            ######### requirements #######################################

            laresult = []
            nkresult = []
            rsresult = []
            ocresult = []
            tfresult = []

            for tfid in tfsid: # select TF only for selected jobtitle

                tf = Tfinfo.objects.get(id=tfid)
                la_get_raw = Tf_la.objects.filter(tf_id=tfid).distinct()
                nk_get_raw = Tf_rs.objects.filter(tf_id=tfid).distinct()
                rs_get_raw = Tf_nk.objects.filter(tf_id=tfid).distinct()
                oc_get_raw = Tf_oc.objects.filter(tf_id=tfid).distinct()

                tfresult.append({'id' : tf.id, 'codetf' : tf.codetf, 'nametf' : tf.nametf})

                for la in la_get_raw:
                    laresult.append({'id' : la.id, 'laboraction' : la.laboraction})

                for nk in nk_get_raw:
                    nkresult.append({'id' : nk.id, 'necessaryknowledge' : nk.requiredskill}) # !!!Swap with RS becouse rosmintrud edition!!!

                for rs in rs_get_raw:
                    rsresult.append({'id' : rs.id, 'requiredskill' : rs.necessaryknowledge}) #  # !!!Swap with NK becouse rosmintrud edition!!!

                for oc in oc_get_raw:
                    ocresult.append({'id' : oc.id, 'othercharacteristic' : oc.othercharacteristic})

            ocresultnew = set( x['othercharacteristic'] for x in ocresult)

            requirements = {'tf' : tfresult,
                            'laboractions' : laresult,
                            'necessaryknowledges' : nkresult,
                            'requiredskills' : rsresult,
                            'othercharacteristics' : ocresultnew,
                            }

            if docx == 'msword-document-download':
                context = { 'generaldatas': generaldatas,
                            'requirements' : requirements,
                            'cmpd' : cmpd,
                            'cmpd0' : cmpd0 }

                media_root = settings.MEDIA_ROOT
                doc = docxtpl.DocxTemplate(media_root+ '/doctemplates/oitemplate.docx')
                doc.render(context)

                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=%s.docx' % re.sub(r'-\d+$', '', generaldatas['slug'])

                doc.save(response)

                return response
                #return redirect(reverse_lazy("org-official-instructions", id=(companyid), pk=(departid), slug=(data) ))

            else:
                return render(request, self.template_name, {'generaldatas': generaldatas,
                                                        'requirements' : requirements,
                                                        'cmpd' : cmpd,
                                                        'cmpd0' : cmpd0,
                                                        'stop_paidactivdate' : stop_paidactivdate,
                                                        'ois_len' : ois_len
                                                        })

class OISaveView(FormView):
    form_class = OICreateForm
    template_name = "companyservices/official-instructions-new.html"

    def form_valid(self, form):
        form.save()

        name = self.request.POST['name']
        tfs = self.request.POST['tfs']
        slug = self.request.POST['slug']
        jt = self.request.POST['jt']
        company = self.request.POST['company']
        departs = self.request.POST['departs']

        return super(OISaveView, self).form_valid(form)

    def get_success_url(self):

        messages.success(self.request, "Должностная инструкция %s была сохранена " % self.request.POST['name'])
        return reverse_lazy('org-official-instructions', kwargs={'id': self.kwargs['id'],
                            'pk': self.kwargs['pk'],'slug': self.kwargs['slug'],})


class OIDeleteView(DeleteView):

    #template_name = "companyservices/departs_confirm_delete.html"

    def get(self, request, *args, **kwargs):

        user = self.request.user
        company_id = self.kwargs['id']
        dep_id =  self.kwargs['pk']

        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            company = Enterprises.objects.get(pk=company_id)
            department = Departs.objects.filter(id=dep_id)[0]

        return render(request, self.template_name, {'company' : company, 'department' : department })


    def get_queryset(self):

        user = self.request.user
        company_id =  self.kwargs['id']
        dep_id =  self.kwargs['pk']

        # check if company belongs auth user
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            return Departs.objects.filter(id=dep_id)


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "Подразделение %s было удалено" % obj.name)
        return super(DepartDeleteView, self).delete(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})

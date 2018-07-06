try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

import json
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView, View, UpdateView
from django.contrib.postgres.search import TrigramSimilarity
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.apps import OIApp # import Official Instruction create app
from psmate.apps.services.forms import SearchPsForm, CvGenForm, GetJTlistForm
###
from django.contrib.auth.models import User
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from time import time

from operator import itemgetter


#from pymorphy2 import units

import re
import random
import pytils
import docxtpl



### Search PS ###

class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated():
         #       return User.objects.none()
        qs = Psinfo.objects.all()

        if self.q:

            qs = qs.filter(nameps__icontains=self.q) # icontains - Case-insensitive

        return qs


class SearchPSView(FormView):
    model = Psinfo
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    success_url = None

    def get(self, request, *args, **kwargs):

        form=SearchPsForm
        data = self.request.GET.get('nameps', None)
        if data != None:
            ps_get = Psinfo.objects.filter(id=data)
            psinfo = ps_get[0]
            tfinfo = Tfinfo.objects.filter(ps_id=psinfo.id).distinct('codetf') # dinstinct delete doubles
            otfinfo = Gtfinfo.objects.filter(ps_id=psinfo.id).distinct('codeotf')
            okzinfo = Okz.objects.filter(ps_id=psinfo.id).distinct('codeokz')
            okvedinfo = Okved.objects.filter(ps_id=psinfo.id).distinct('codeokved')

            mixed_tf_otf = []

            # for OTF -TF dividing in table used nex list:
            # [[otf1,[tf1, tf2]],[otf2,[tf1, tf2]]]
            for otf in otfinfo:
                mixed_tf = []

                for tf in tfinfo:
                    if tf.nameotf == otf.nameotf:
                        mixed_tf.append(tf)

                mixed_tf_otf.append([otf, mixed_tf])

            return render(request, self.template_name, {'psinfo': psinfo,
                                                        'mixed_tf_otf': mixed_tf_otf,
                                                        'okzinfo': okzinfo,
                                                        'okvedinfo': okvedinfo,
                                                        'ngshow' : 'true', # ng-show for id="showps
                                                        'form': form})
        return render(request, self.template_name, {'form': form})

##################

###CV generator###


class CvEditView(UpdateView):

    template_name = 'services/generator-cv-resume.html'
    form_class = CvGenForm
    model = User
    # success_url = None


    def get_object(self, queryset=None):

        user = self.request.user
        if not user.is_anonymous :
            if user.profiles.fl_tlph_mob == None: # if user not set settings
                user.profiles.fl_tlph_mob = ''
            if user.profiles.fl_otch == None:
                user.profiles.fl_otch = ''
            if user.profiles.fl_pd_date == None:
                user.profiles.fl_pd_date = ''
            if user.profiles.fl_adress_real == None:
                user.profiles.fl_adress_real = ''

            return user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CvEditView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(CvEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('presentation-cv-resume')

    def form_valid(self, form):
        self.object = self.get_object()

        return super(CvEditView, self).form_valid(form)


class LoadPS(View):

    def get(self, request, *args, **kwargs):

        data = self.request.GET.get('id', None)

        if data != None:
            ps_get = Psinfo.objects.filter(otraslid_id=data)
            jtresult = []

            for ps in ps_get:

                jt_get = Jobtitles.objects.filter(ps_id=ps.id).distinct('jobtitle')

                for jt in jt_get:

                    jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle,
                                     # 'pspurposekind' : ps.pspurposekind,
                                     'nameps' : ps.nameps, 'psregnum' : ps.psregnum,
                                     'ps_id' : ps.id,
                                     'pspurposekind' : ps.pspurposekind})

            return JsonResponse(jtresult, safe=False)


class LoadCompt(View):

    def get(self, request, *args, **kwargs):

        t0 = time()

        data = self.request.GET.getlist('psvars', None)

        if data != None:

            tf_get_raw = Tfinfo.objects.filter(ps_id=data[0])

            otf_get_raw = Jobtitles.objects.filter(id=data[1]) # get OTF by jobtitle

            otflist = []
            maintfresult = []

            for otf in otf_get_raw:

                otflist.append(otf.gtf_id)

            for tf in tf_get_raw: # select TF only for selected jobtitle (used in color sheme in generator-cv)

                laresult = []
                nkresult = []
                rsresult = []
                ocresult = []

                la_get_raw = Tf_la.objects.filter(tf_id=tf.id)
                nk_get_raw = Tf_rs.objects.filter(tf_id=tf.id)
                rs_get_raw = Tf_nk.objects.filter(tf_id=tf.id)
                oc_get_raw = Tf_oc.objects.filter(tf_id=tf.id)

                for la in la_get_raw:
                    laresult.append({'id' : la.id, 'laboraction' : la.laboraction})

                for nk in nk_get_raw:
                    nkresult.append({'id' : nk.id, 'necessaryknowledge' : nk.requiredskill}) # !!!Swap with RS becouse rosmintrud edition!!!

                for rs in rs_get_raw:
                    rsresult.append({'id' : rs.id, 'requiredskill' : rs.necessaryknowledge}) #  # !!!Swap with NK becouse rosmintrud edition!!!

                for oc in oc_get_raw:
                    ocresult.append({'id' : oc.id, 'othercharacteristic' : oc.othercharacteristic})

                # time test
                #t1 = time()
                #time_res = t1 - t0
                #print(time_res)

                #dynamic  mdbootstrap class for TF matched of JT:


                tfsel = ''
                if tf.gtf_id in otflist:

                    tfsel = 'card info-color white-text mb-0 py-2 z-depth-2'

                maintfresult.append({'id' : tf.id, 'codetf' : tf.codetf,
                                     'nametf' : tf.nametf, 'tfsel' : tfsel, # tfcell use for color ligth of jobtitels tf's
                                     'laboractions' : laresult,
                                     'necessaryknowledges' : nkresult,
                                     'requiredskills' : rsresult,
                                     'othercharacteristics' : ocresult,

                                     })


            return JsonResponse(maintfresult, safe=False)

#####################


#### Load CV ########


class LoadCV(View):

    def get(self, request, *args, **kwargs):

        usercv = self.request.user.profiles.resume

        return JsonResponse(usercv, safe=False)


###CV Presentation###

class CvPresentView(ListView):

    template_name = 'services/presentation-cv-resume.html'
    model = User

    def get_context_data(self, **kwargs):

        udata = super(CvPresentView, self).get_context_data(**kwargs)
        user = self.request.user

        if not user.is_anonymous :
            if user.profiles.fl_tlph_mob == None: # if user not set settings
                user.profiles.fl_tlph_mob = ''
            if user.profiles.fl_otch == None:
                user.profiles.fl_otch = ''
            if user.profiles.fl_pd_date == None:
                user.profiles.fl_pd_date = ''
            if user.profiles.fl_adress_real == None:
                user.profiles.fl_adress_real = ''

            cv =user.profiles.resume # get resume - JSONb field

            cvcleared = []

            key,value = 'selected', True
            for i in cv:

                quali = []

                for s in i['Quali'] :

                    tf_arr = []
                    la_arr = []
                    rs_arr = []
                    nk_arr = []
                    oc_arr = []
                    # found and append only selected competences in cv
                    for tf in s['FL_cv_TF']:

                        if key in tf and value == tf[key]:
                            tf_arr.append({'nametf' : tf['nametf'], 'codetf' : tf['codetf']})
                            # append if tf_arr != []

                        for la in tf['laboractions'] :
                            if key in la and value == la[key]:
                                la_arr.append({'laboraction' : la['laboraction']})

                        for rs in tf['requiredskills'] :
                            if key in rs and value == rs[key]:
                                rs_arr.append({'requiredskill' : rs['requiredskill']})

                        for nk in tf['necessaryknowledges'] :
                            if key in nk and value == nk[key]:
                                nk_arr.append({'necessaryknowledge' : nk['necessaryknowledge']})

                        for oc in tf['othercharacteristics'] :
                            if key in oc and value == oc[key]:
                                oc_arr.append({'othercharacteristic' : oc['othercharacteristic']})

                    quali.append({ 'PS' :s['FL_cv_PS'],
                                   'Otrasl' :s['FL_cv_Otrasl'],
                                   'tf' : tf_arr,
                                   'la' : la_arr,
                                   'rs' : rs_arr,
                                   'nk' : nk_arr,
                                   'oc' : oc_arr
                                })

                cvcleared.append(
                                {'companyname' : i['FL_cv_companyName'],
                                'startdate' :   i['FL_cv_WorkStartDate'],
                                'enddate' :     i['FL_cv_WorkEndDate'],
                                'keyskills' :    i['KeySkills'],
                                'quali' : quali})

            return {'cvcleared' :cvcleared}


###Get competences - search from index.html###

### Load Jobtitles for autocomplete  ###
class AutoLoadJT(View):

    def get(self, request, *args, **kwargs):

        data = self.request.GET.get('search', None)

        if data != None:

            #jts = Jobtitles.objects.filter(jobtitle__icontains=data).distinct('jobtitle')[:10]

            jts = Jobtitles.objects.annotate(
                similarity=TrigramSimilarity('jobtitle', data),).filter(
                similarity__gt=0.3).order_by('-similarity')

            jtresult = []
            for jt in jts:
                jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle})

            return JsonResponse(jtresult, safe=False)


class SearchJT(FormView):
    template_name = 'index.html'
    form_class = GetJTlistForm

    def form_valid(self, form):
        jobtitle = form.cleaned_data.get('jobtitle')

        return redirect('search-jobtitles', jobtitle)


class ShowJTlist(ListView):

    template_name = 'services/jobtitles-list.html'
    model = Jobtitles
    context_object_name = "jtresult"
    queryset = ''

    paginate_by = 25

    def get_paginate_by(self, queryset):
            """
            Paginate by specified value in querystring, or use default class property value.
            """
            return self.request.GET.get('paginate_by', self.paginate_by)


    def get_queryset(self,  *args, **kwargs):

        search_data = self.request.GET.get('search', None)

        ### Generate xml sitemap for jt links ###
#         jt_get = Jobtitles.objects.all()
#         url_count = 0
#         with open ('sitemap.xml', 'a') as sitemap:
#             print('write xml')
#             for jt in jt_get:
#                 jt_slug = pytils.translit.slugify(jt.jobtitle) + '-' + str(jt.id)
#
#                 sitemap.write("""<url>
#     <loc>https://qualinfo.ru/competences/%s/</loc>
#     <lastmod>2018-03-28</lastmod>
#     <changefreq>monthly</changefreq>
#     <priority>0.6</priority>
# </url>
# <url>
#     <loc>https://qualinfo.ru/official-instructions/%s/</loc>
#     <lastmod>2018-03-28</lastmod>
#     <changefreq>monthly</changefreq>
#     <priority>0.6</priority>
# </url>
# """ % (jt_slug, jt_slug ))
#
#                 url_count +=2
#         print(url_count)

        jtresult = []

        if search_data:

            search_data = search_data.strip()
            search_data = ' '.join(search_data.split())

            #jt_get = Jobtitles.objects.filter(jobtitle__icontains=search_data).distinct('id')
            jt_get = Jobtitles.objects.annotate(
                similarity=TrigramSimilarity('jobtitle', search_data),).filter(
                similarity__gt=0.3).order_by('-similarity')
            if not jt_get:
                messages.warning(self.request, "Должность <b>%s</b> не найдена, уточните запрос" % search_data)

            for jt in jt_get:

                ps = Psinfo.objects.filter(id=jt.ps_id)
                gtf = Gtfinfo.objects.get(id=jt.gtf_id)

                otrasl = ps[0].otraslid
                ### Slug save
                jt.slug = pytils.translit.slugify(jt.jobtitle) + '-' + str(jt.id)
                jt.save()
                ###
                jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle, 'nameotf' : jt.nameotf,
                                 'slug' : jt.slug,
                                 # 'pspurposekind' : ps.pspurposekind,
                                 'levelofquali' : gtf.levelofquali,
                                 'codeotf' : gtf.codeotf,
                                 'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum,
                                 'otraslname' : otrasl.name,
                                 'otraslicon' : otrasl.icon
                                 },
                    )


            return sorted(jtresult, key=itemgetter('jobtitle'))

        else:

            num_jt =  Jobtitles.objects.all().count() # all entities of jobtitles
            rand_entities = random.sample(range(num_jt), 10)
            random_jt = Jobtitles.objects.filter(id__in=rand_entities)

            for jt in random_jt:

                ps = Psinfo.objects.filter(id=jt.ps_id)
                gtf = Gtfinfo.objects.get(id=jt.gtf_id)

                otrasl = ps[0].otraslid
                ### Slug save
                jt.slug = pytils.translit.slugify(jt.jobtitle) + '-' + str(jt.id)
                jt.save()
                ###
                jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle, 'nameotf' : jt.nameotf,
                                 'slug' : jt.slug,
                                 # 'pspurposekind' : ps.pspurposekind,
                                 'levelofquali' : gtf.levelofquali,
                                 'codeotf' : gtf.codeotf,
                                 'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum,
                                 'otraslname' : otrasl.name,
                                 'otraslicon' : otrasl.icon,
                                 'jtrandom' : True,
                                 },
                    )

            return sorted(jtresult, key=itemgetter('jobtitle'))



class JTDetailsView(ListView):

    template_name = 'services/jobtitle-details.html'
    model = Jobtitles

    def get(self, request, *args, **kwargs):

        jt_slug =  self.kwargs['slug']

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

            return render(request, self.template_name, {'jtresult': jtresult})


class OfficialInstructions(ListView):

    template_name = 'services/official-instructions.html'
    model = Jobtitles

    def get(self, request, *args, **kwargs):

        #t0 = time()

        data =  self.kwargs['slug']
        docx =  self.kwargs['docx']
        tfsid = [int(x) for x in self.request.GET.getlist('tfids')] # tf id's from url get whish user check from jt tf checkbox

        if data != None:

            jt = Jobtitles.objects.filter(slug=data)

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id)
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id)
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id)
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id)
            gtfs = Jobtitles.objects.filter(jobtitle=jt[0].jobtitle).filter(ps_id=jt[0].ps_id).exclude(nameotf=jt[0].nameotf)

            # if user go to url without parameters
            if not tfsid:
                tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
                tfsid = [x.id for x in tfs]

            otrasl = ps[0].otraslid

            generaldatas = []

            oi_app = OIApp()
            ##### nowdate in roditelny padezh(need for docx generation)##

            rod_nowdate = oi_app.nowdate_rod()

            generaldatas = {
                    'slug' : data,
                    'jobtitleid' : jt[0].id,
                    'jobtitle' : jt[0].jobtitle,
                    'jobtitlerod' : jt[0].jobtitle_rod,
                    'nameotf' : jt[0].nameotf,
                    'gtfs':gtfs,
                    'pspurposekind' : ps[0].pspurposekind,
                    'nameps' : ps[0].nameps,
                    'psregnum' : ps[0].psregnum,
                    'ps_id' : ps[0].id,
                    'psordernum' : ps[0].psordernum,
                    'psdateappr' : ps[0].psdateappr,
                    'otraslname' : otrasl.name,
                    'otraslicon' : otrasl.icon,
                    'educationalreqs' : educationalreqs,
                    'reqworkexperiences' : reqworkexperiences,
                    'specialconditions' : specialconditions,
                    'othercharacts' : othercharacts,
                    'today' : rod_nowdate['today'],
                    'month': rod_nowdate['rod_month'],
                    'year' :rod_nowdate['year']
                    }

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

            # get company data
            cmpd = oi_app.fake_cmpd(laresult, nkresult, rsresult, ocresult, tfresult)

##########################
            requirements = {'tf' : tfresult,
                            'laboractions' : laresult,
                            'necessaryknowledges' : nkresult,
                            'requiredskills' : rsresult,
                            'othercharacteristics' : ocresultnew,
                            }


            ### Doc download part ###
            if docx == 'msword-document-download':
                context = { 'generaldatas': generaldatas,
                            'requirements' : requirements,
                            'cmpd' : cmpd
                          }

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
                                                            'cmpd' :cmpd
                                                            })
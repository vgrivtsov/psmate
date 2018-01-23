#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from psmate.models import Okved
from psmate.models import Okz
from psmate.models import Eks
from psmate.models import Okpdtr
from psmate.models import Okso
from psmate.models import Educationalreqs
from psmate.models import Jobtitles
from psmate.models import Reqworkexperiences
from psmate.models import Specialconditions
from psmate.models import Othercharacts
from psmate.models import Gtfinfo
from psmate.models import Tfinfo
from psmate.models import Psinfo
from psmate.models import Tf_la
from psmate.models import Tf_oc
from psmate.models import Tf_nk
from psmate.models import Tf_rs

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Since the CSV headers match the model fields,
        # you only need to provide the file's path
        # Educationalreqs.objects.from_csv('./predata/csv/educationalreqs.csv', delimiter=';')        
        # self.stdout.write("Import educationalreqs.csv.csv to Postresql OK")
        # 
        # Eks.objects.from_csv('./predata/csv/EKS.csv', delimiter=';')        
        # self.stdout.write("Import EKS.csv to Postresql OK")
        # 
        # Gtfinfo.objects.from_csv('./predata/csv/GTFINFO.csv', delimiter=';')        
        # self.stdout.write("Import GTFINFO.csv to Postresql OK")                
        # 
        # Jobtitles.objects.from_csv('./predata/csv/jobtitles.csv', delimiter=';')        
        # self.stdout.write("Import jobtitles.csv to Postresql OK")        
        # 
        # Okpdtr.objects.from_csv('./predata/csv/OKPDTR.csv', delimiter=';')        
        # self.stdout.write("Import OKPDTR.csv to Postresql OK")
        # 
        # Okso.objects.from_csv('./predata/csv/OKSO.csv', delimiter=';')        
        # self.stdout.write("Import OKSO.csv to Postresql OK")        
        # 
        # Okved.objects.from_csv('./predata/csv/OKVED.csv', delimiter=';')        
        # self.stdout.write("Import OKVED.csv to Postresql OK")
        # 
        # Okz.objects.from_csv('./predata/csv/OKZ.csv', delimiter=';')        
        # self.stdout.write("Import OKZ.csv to Postresql OK")        
        # 
        # Othercharacts.objects.from_csv('./predata/csv/othercharacts.csv', delimiter=';')        
        # self.stdout.write("Import othercharacts.csv to Postresql OK")                

        Psinfo.objects.from_csv('./predata/csv/PSINFO.csv', delimiter=';')        
        self.stdout.write("Import PSINFO.csv to Postresql OK")
        # 
        # Reqworkexperiences.objects.from_csv('./predata/csv/reqworkexperiences.csv', delimiter=';')        
        # self.stdout.write("Import reqworkexperiences.csv to Postresql OK")
        # 
        # Specialconditions.objects.from_csv('./predata/csv/specialconditions.csv', delimiter=';')        
        # self.stdout.write("Import specialconditions.csv to Postresql OK")
        # 
        # Tf_la.objects.from_csv('./predata/csv/tf_la.csv', delimiter=';')        
        # self.stdout.write("Import tf_la.csv to Postresql OK")
        # 
        # Tf_nk.objects.from_csv('./predata/csv/tf_nk.csv', delimiter=';')        
        # self.stdout.write("Import tf_nk.csv to Postresql OK")
        # 
        # Tf_oc.objects.from_csv('./predata/csv/tf_oc.csv', delimiter=';')        
        # self.stdout.write("Import tf_oc.csv to Postresql OK")
        # 
        # Tf_rs.objects.from_csv('./predata/csv/tf_rs.csv', delimiter=';')        
        # self.stdout.write("Import tf_rs.csv to Postresql OK")
        # 
        # Tfinfo.objects.from_csv('./predata/csv/TFINFO.csv', delimiter=';')        
        # self.stdout.write("Import TFINFO.csv to Postresql OK")

  

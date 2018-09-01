from django.apps import AppConfig

import pymorphy2
import locale
import re
import random
from datetime import datetime
from mimesis import Business, Person
from mimesis.builtins import RussiaSpecProvider



class ServicesConfig(AppConfig):
    name = 'services'


class OIApp:

    def __init__(self):

        self.morph = pymorphy2.MorphAnalyzer()


    def make_jobtitlerod(self, jt0):
        #make jobtitle Roditelny paezh

        jt_rod = []


        #cut non need padezh string beenween '( )'
        pattern = re.compile("[\(\[].*?[\)\]]")
        if re.findall(pattern, jt0):
            cuttedstring = re.findall(pattern, jt0)[0]
        else:
            cuttedstring = ''

        cleared_jt = re.sub("[\(\[].*?[\)\]]", "", jt0)

        pos_list = ['NOUN', 'ADJF', 'ADJS', 'PRTF', 'PRTS']
        case_list = []

        for i in cleared_jt.split(' '):
            p = self.morph.parse(i)[0]
            print(p, p.tag.POS, p.tag.case)
            if p.tag.POS in pos_list and p.tag.case == 'nomn' or p.tag.case == 'loct' and p.tag.number == 'sing': # Chast' rechi & padezh

                #print(jt_rod_word)
                if p.inflect({'gent'}) :

                    changed_word = p.inflect({'sing', 'gent'}).word

                    if changed_word == 'риска-менеджера':
                        changed_word = 'риск-менеджера'

                    jt_rod.append(changed_word)

                else:

                    jt_rod.append(i)

            else:
                jt_rod.append(i)

        jobtitlerod = ' '.join(jt_rod) + ' '+cuttedstring

        return jobtitlerod


    def fake_cmpd(self, ps, okz, laresult, nkresult, rsresult, ocresult, tfresult):
        #### FAKE COMPANY DATA ###
        # person = Person('ru')
        # full_name = person.full_name()
        # ruspec = RussiaSpecProvider()
        # e_otch_ul = ruspec.patronymic()
        # e_name_ul, e_fam_ul = full_name.split(" ")[-2:]
        ##########################

        #check if jobtitle CEO
        codeokz = okz[0].codeokz
        ceo = False
        if codeokz[0] == "1":
            ceo = True

        developer = (ps[0].responsibledeveloper).split(",")[0]
        head = ps[0].head
        headname = ps[0].headname
        e_fam_ul, e_name_ul, e_otch_ul = 'Пушкин','Александр','Сергеевич'
        if headname:
            e_fam_ul, e_name_ul, e_otch_ul = headname.split(" ")

        e_director = 'Генеральный директор'
        e_director_gent = 'Генерального директора'
        e_director_datv = 'Генеральному директору'

        if head:
            e_director = head
            head_split = head.split(" ")
            e_director_gent = [self.morph.parse(w)[0].inflect({'gent'}).word for w in head_split]
            e_director_gent = " ".join(e_director_gent)
            e_director_datv = [self.morph.parse(w)[0].inflect({'datv'}).word for w in head_split]
            e_director_datv = " ".join(e_director_datv)


        def get_init_words(attr, arr):

            init_words = [ x[attr] for x in arr]
            raw_words = []
            for sentense in init_words:
                cleared = re.sub(r'[^\w]', ' ', sentense)
                splitted = cleared.strip().split(" ")

                raw_words += splitted
            cleared_from_empty = [x.lower() for x in raw_words if not x == '']
            adjective = []
            for word in cleared_from_empty:
                init_word = self.morph.parse(word)[0]
                if init_word.tag.POS == 'ADJF':
                    adjective.append(init_word.normalized)


            if adjective == []:
                return [self.morph.parse('Новые')[0],]

            return adjective

        all_words =(get_init_words('laboraction', laresult) +
                    get_init_words('necessaryknowledge', nkresult) +
                    get_init_words('nametf', tfresult)
                    )

        def gen_depname_data(word_arr):

            word_list = ['технологии', 'связи', 'исследования', 'компетенции']
            randomchoise_first = random.choice(word_arr)
            randomchoise_second = random.choice(word_list)

            first_word = randomchoise_first.inflect({'plur'}).word


            return first_word.capitalize() + ' ' +  randomchoise_second

        business = Business('ru')
        # e_name =  business.company().replace('«', '').replace('»', '') # for fake data
        e_name = developer
        depname = gen_depname_data(all_words)
        # e_op_form = business.company_type(abbr=True) # fake data

        cheef = 'Начальник'
        cheef_name = 'Иванов'
        cheef_otch = 'Иван'
        cheef_fam = 'Петрович'
        d_cheef_datv = 'Начальнику'

        cmpd = {  'e_name' : e_name,
                  # 'e_op_form' : e_op_form,
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
                  'd_cheef_datv' : d_cheef_datv,
                  'ceo': ceo
               }

        return cmpd


    def nowdate_rod(self):

        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        today = datetime.now().strftime("%d %B %Y").lower()

        today, month, year = today.split(' ')

        rod_month = self.morph.parse(month)[0].inflect({'gent'}).word

        rod_nowdate = {'today' : today,
                'rod_month' : rod_month,
                'year' : year
               }

        return rod_nowdate

from django.apps import AppConfig

import pymorphy2
import re
import random
from mimesis import Business, Person
from mimesis.builtins import RussiaSpecProvider


class ServicesConfig(AppConfig):
    name = 'services'


class OIApp:

    def __init__(self):
        #self.jt0 = jt0
        self.morph = pymorphy2.MorphAnalyzer()

    # morph = pymorphy2.MorphAnalyzer()

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
            if p.tag.POS in pos_list and p.tag.case == 'nomn' and p.tag.number == 'sing': # Chast' rechi & padezh

                #print(jt_rod_word)
                if p.inflect({'gent'}) :

                    changed_word = p.inflect({'sing', 'gent'}).word
                    if changed_word == 'риска-менеджера':
                        changed_word = 'риск-менеджера'
                    if changed_word == 'бренда-менеджера':
                        changed_word = 'бренд-менеджера'
                    if changed_word == 'брэнда-менеджера':
                        changed_word = 'брэнд-менеджера'
                    if changed_word == 'поварова':
                        changed_word = 'поваров'
                    if changed_word == 'котлова':
                        changed_word = 'котлов'
                    if changed_word == 'чокерноя':
                        changed_word = 'чокерной'
                    if changed_word == 'игрового':
                        changed_word = 'игровой'

                    jt_rod.append(changed_word)

                else:

                    jt_rod.append(i)

            else:
                jt_rod.append(i)

        jobtitlerod = ' '.join(jt_rod) + ' '+cuttedstring

        return jobtitlerod


    def fake_cmpd(self, laresult, nkresult, rsresult, ocresult, tfresult):
#### FAKE COMPANY DATA ###
        person = Person('ru')
        full_name = person.full_name()
        ruspec = RussiaSpecProvider()
        e_otch_ul = ruspec.patronymic()
        e_name_ul, e_fam_ul = full_name.split(" ")[-2:]

        def get_init_words(attr, arr):

            init_words = [ x[attr] for x in arr]
            raw_words = []
            for sentense in init_words:
                cleared = re.sub(r'[^\w]', ' ', sentense)
                splitted = cleared.strip().split(" ")

                raw_words += splitted
            cleared_from_empty = [x.lower() for x in raw_words if not x == '']

            return cleared_from_empty

        all_words =(get_init_words('laboraction', laresult) +
                    get_init_words('necessaryknowledge', nkresult) +
                    get_init_words('requiredskill', rsresult) +
                    get_init_words('othercharacteristic', ocresult) +
                    get_init_words('nametf', tfresult)
                    )

        def gen_depname_data(word_arr):

            nouns = []
            adjective = []

            for k in word_arr:
                init_word = self.morph.parse(k)[0]
                if init_word.tag.POS == 'NOUN':
                    nouns.append(init_word.normalized)
                if init_word.tag.POS == 'ADJF':
                    adjective.append(init_word.normalized)

            plur_singl = ['plur','sing']
            kind = ['masc','femn','neut']

            rand_plursing = random.choice(plur_singl)
            rand_kind = random.choice(kind)

            nouns_x = [a for a in nouns if a.tag.gender == rand_kind]

            randomchoise_first = random.choice(adjective)
            randomchoise_sec =   random.choice(nouns_x)

            if rand_plursing == 'plur':
                first_word = randomchoise_first.inflect({ rand_plursing}).word
                second_word = randomchoise_sec.inflect({rand_plursing}).word

            else:
                first_word = randomchoise_first.inflect({ rand_kind}).word
                second_word = randomchoise_sec.inflect({rand_plursing}).word

            return first_word.capitalize() + ' ' + second_word

        business = Business('ru')
        e_name =  business.company()
        depname = gen_depname_data(all_words)

        cmpd = {  'e_name' : e_name,
                  'e_fam_ul' : e_fam_ul,
                  'e_name_ul' : e_name_ul,
                  'e_otch_ul' : e_otch_ul,
                  'depname' : depname,
                }

        return cmpd
# coding=utf8
import os

import django
import names

os.environ['DJANGO_SETTINGS_MODULE'] = "ipt_connect.settings"

django.setup()

from IPT2016 import models as m16
from IPT2017 import models as m17
from FPT2017 import models as f17
from IPT2018 import models as m18

# IPT2016

participants = m16.Participant.objects.all()

for p in participants:
    if 1:
        p.name = names.get_first_name()
        p.surname = names.get_last_name()
        p.gender = "D"
        p.email = "toto@toto.com"
        p.birthdate = '1900-01-31'
        p.photo = 'id_photo/gcof.png'
        p.passport_number = '1234'
        p.diet = 'NO'
        p.tourism = 'TOURISM_0'
        p.shirt_size = 'L'
        p.mixed_dorm = 'False'
        p.remark = 'hohoho'
        p.hotel_room = 'No'
        p.check_in = 'True'

        p.save()

# IPT2017
participants = m17.Participant.objects.all()

for p in participants:
    if 1:
        p.name = names.get_first_name()
        p.surname = names.get_last_name()
        p.gender = "D"
        p.email = "toto@toto.com"
        p.phone_regex = '+123456'
        p.phone_number = '1234'
        p.birthdate = '1900-01-31'
        p.photo = 'id_photo/gcof.png'
        p.passport_number = '1234'
        p.diet = 'NO'
        p.tourism = 'TOURISM_0'
        p.shirt_size = 'L'
        p.mixed_gender_accomodation = 'False'
        p.remark = 'hohoho'
        p.hotel_room = 'No'
        p.check_in = 'True'

        p.save()

# IPT2018
participants = m18.Participant.objects.all()

for p in participants:
    if 1:
        p.name = names.get_first_name()
        p.surname = names.get_last_name()
        p.gender = "D"
        p.email = "toto@toto.com"
        p.phone_regex = '+123456'
        p.phone_number = '1234'
        p.birthdate = '1900-01-31'
        p.photo = 'id_photo/gcof.png'
        p.passport_number = '1234'
        p.diet = 'NO'
        p.tourism = 'TOURISM_0'
        p.shirt_size = 'L'
        p.mixed_gender_accomodation = 'False'
        p.flight_number_arrival = '1234'
        p.date_hour_arrival = '1234'
        p.arrival_airport = '1234'
        p.flight_number_departure = '1234'
        p.remark = 'hohoho'
        p.room_number = '1234'

        p.save()

# FPT2017

participants = f17.Participant.objects.all()
for p in participants:
    if 1:
        p.name = names.get_first_name()
        p.surname = names.get_last_name()
        p.gender = "D"
        p.email = "toto@toto.com"
        p.birthdate = '1900-01-31'
        p.photo = 'id_photo/gcof.png'
        p.passport_number = '1234'
        p.diet = 'NO'
        p.tourism = 'TOURISM_0'
        p.shirt_size = 'L'
        p.remark = 'hohoho'

        p.save()

# Jurys
jurys = f17.Jury.objects.all()
for j in jurys:
    j.name = names.get_first_name()
    j.surname = names.get_last_name()
    j.email = '1234'
    j.save()

jurys = m17.Jury.objects.all()
for j in jurys:
    j.name = names.get_first_name()
    j.surname = names.get_last_name()
    j.email = '1234'
    j.save()

jurys = m18.Jury.objects.all()
for j in jurys:
    j.name = names.get_first_name()
    j.surname = names.get_last_name()
    j.email = '1234'
    j.save()

jurys = m16.Jury.objects.all()
for j in jurys:
    j.name = names.get_full_name()
    j.email = '1234'
    j.save()

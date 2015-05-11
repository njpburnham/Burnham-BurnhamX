# -*- coding: utf-8 -*-
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'burnhamx.settings'
from django.conf import settings
from extension.models import Opportunity, Association, Users
from datetime import date, timedelta, datetime

import pprint

import csv



with open("carson.csv", "rU") as csv_file:
  reader = csv.DictReader(csv_file)
  for row in reader:
    curr_opp = Opportunity.objects.filter(siebel_id=row['Opty'])
    user = Users.objects.filter(email=row['Email'])
    if not user:
      user = Users()
      user.email = row['Email']
      user.save()
    else:
      user = user[0]
    if curr_opp:
      user.opportunities.add(curr_opp[0])
      print "Added: %s" % curr_opp[0]
    else:
      pprint.pprint(row['Opty'])



import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'burnhmax.settings'
from django.conf import settings
from extension.models import Opportunity, Associationfrom datetime import date, timedelta, datetime

import pprint


# billing_type = models.ForeignKey("BillingType")
# sale_price = models.DecimalField(max_digits=6, decimal_places=2)
# purch_price = models.DecimalField(max_digits=6, decimal_places=2)
# start_date = models.DateField()
# end_date = models.DateField()


import csv
# -*- coding: utf-8 -*-
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'burnhamx.settings'
from django.conf import settings
from extension.models import Opportunity, Association, Users
from datetime import date, timedelta, datetime
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from apiclient import errors
import httplib2
import pprint

import csv

SERVICE_ACCOUNT_EMAIL = "643460748243-5j6p8t6373k4jqheajld7um4s7r64pi2@developer.gserviceaccount.com"

def GetThread(service, user_id, thread_id):
  """Get a Thread.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    thread_id: The ID of the Thread required.

  Returns:
    Thread with matching ID.
  """
  try:
    thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
    messages = thread['messages']
    print ('thread id: %s - number of messages '
           'in this thread: %d') % (thread['id'], len(messages))
    return thread
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format="minimal").execute()
    return message['threadId']
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def create_gmail_service(user_email):
    """
    Builds and returns a Gmail service object authorized with the
    application's service account.
    Returns:
        Gmail service object.
    """
    f = file('bprivate.pem', 'rb')
    key = f.read()
    f.close()
    credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key, scope='https://mail.google.com/', sub=user_email)
    http = httplib2.Http()
    http = credentials.authorize(http)
     
    return build('gmail', 'v1', http=http)

# with open("assoc.csv", "rb") as csv_file:
#   reader = csv.DictReader(csv_file)
#   services = {}
#   for row in reader:
#     user =row['user']
#     email_id = row['email_id']
#     siebel_id = row['siebel_id']
#     already_exists = Association.objects.filter(email_id=email_id)
#     if not already_exists.exists():

#       curr_opp = Opportunity.objects.filter(siebel_id=row['siebel_id'])
#       if curr_opp:
#         if user in services:
#           service = services[user]
#         else:
#           service = create_gmail_service(user)
#           services[user] = service

#         thread_id = GetMessage(service, user, email_id)
#         if not thread_id:
#           thread_id = "99"
#         Association.objects.create(
#               email_id=email_id,
#               thread_id=thread_id,
#               created_user=user,
#               is_active=True,
#               opportunity=curr_opp[0]
#           )
#       else:
#         print "No Opp in DB: ", row
#     else:
#       print "already exists: ", row


# with open("opty1.csv", 'rb') as csv_file:
#   reader = csv.DictReader(csv_file, delimiter="|")
#   #NAME|Status|Street|City|State|Zip|SiebelId
  
#   count = 0
#   for row in reader:
#     count += 1
#     opp = Opportunity()
#     opp.name = str(row.get('NAME','N/A'))
#     opp.status= str(row.get('Status', 'N/A'))
#     opp.street = str(row.get('Street', 'N/A'))
#     opp.city = str(row.get('City', 'N/A'))
#     opp.state = str(row.get('State', "N/A"))
#     opp.zip_code = str(row.get('Zip', 'N/A'))
#     opp.siebel_id = str(row.get('SiebelId', "NULL"))
#     opp.save()
#     if count % 1000 == 0:
#       print count



with open('OptyVis4.csv', 'rb') as csv_file:
  reader = csv.DictReader(csv_file)
  services = {}
  count = 0
  print "Started Processing"
  for row in reader:
    count += 1
    user = Users.objects.filter(email=row['EMAIL'])
    if user:
      opp = Opportunity.objects.filter(siebel_id=row["OPTY"])
      if opp:
        user = user[0]
        opp =  opp[0]
        user.opportunities.add(opp)
        user.save()
      else:
        print "User %s OPP %s" % (row['EMAIL'], row['OPTY'])
    else:
      user = Users()
      user.email = row['EMAIL']
      user.is_active = True
      user.save()
      opp = Opportunity.objects.filter(siebel_id=row["OPTY"])
      if opp:
        opp = opp[0]
        user.opportunities.add(opp)
        user.save()
      else:
        print "User %s OPP %s" % (row['EMAIL'], row['OPTY'])

    if count % 1000 == 0:
      print count

    





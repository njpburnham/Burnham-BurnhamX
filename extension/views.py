import httplib2
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from extension.models import Opportunity, Association
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from google.appengine.api import users
from google.appengine.api import taskqueue
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from apiclient import errors



SERVICE_ACCOUNT_EMAIL = "643460748243-5j6p8t6373k4jqheajld7um4s7r64pi2@developer.gserviceaccount.com"


def associate(request, thread_id, message_id):
  """
  Inputs:
    - request: Django Request Object
    - thread_id: The Gmail Thread ID. Each thread has a unique thread and is located in the URl
    - message_id: The individual message that the user was looking at when they clicked associate
  
  If the user chooses an OPTY to associate the email, the application will associate and direct to a thanks page (5 second close timer)

  """
  if not users.get_current_user():
    return HttpResponseRedirect(users.create_login_url(request.path))

  if request.method == "GET":
    variables = {}
    # The association must not only be related to the thread, but also active
    curr_assoc = Association.objects.filter(thread_id=thread_id, is_active=True)
    if curr_assoc.exists():
      variables['association'] = curr_assoc[0]
      return render_to_response("extension/already_associated.html", variables, context_instance=RequestContext(request))
    variables['user'] = users.get_current_user()
    return render_to_response("extension/associate.html", variables, context_instance=RequestContext(request))
  else:
    variables = {}
    curr_opp = Opportunity.objects.get(pk=request.POST['opp'])
    # Push onto queue
    # Just a single association
    
    association = Association()
    association.thread_id = thread_id
    association.email_id = message_id
    association.opportunity = curr_opp
    association.created_user = users.get_current_user()
    association.save()
    taskqueue.add(url='/extension/pastAssociation/', params={"thread_id": thread_id, "user": users.get_current_user()})
    
    return redirect("/extension/thanks")

def thanks(request):
  return render_to_response("extension/thanks.html")


def bulk_associate(request, thread_ids):
  """
  Inputs:


  


  """
  if not users.get_current_user():
    return HttpResponseRedirect(users.create_login_url(request.path))

  if request.method == "GET":
    variables = {}
    
    for thread_id in thread_ids.split('_'):
      if Association.objects.filter(thread_id=thread_id).count() > 0:
        return render_to_response("extension/bulk_already_associated.html", variables, context_instance=RequestContext(request))

    opps = Opportunity.objects.all()
    variables['opps'] = opps
    return render_to_response("extension/associate.html", variables, context_instance=RequestContext(request))
  
  else:
    variables = {}
    curr_opp = Opportunity.objects.get(pk=request.POST['opp'])
    # this means it's a bulk association
    
    for thread_id in thread_ids.split('_'):
      association = Association()
      association.thread_id = thread_id
      association.email_id = "" #TODO
      association.opportunity = curr_opp
      association.created_user = users.get_current_user()
      association.save()
  
    return redirect("/extension/thanks")

def unassociate(request):
  if request.method == "POST":
    association = Association.objects.get(pk=request.POST['association'])
    association.is_active = False
    association.save()

  return redirect("/extension/thanks")




#
@csrf_exempt
def past_association(request):
  # create gmail service object
  # loop through and check all messages in threads
  thread_id = request.POST['thread_id']
  user = request.POST['user']
  service = create_gmail_service(user)
  thread = GetThread(service, user, thread_id)
  if len(thread['messages']) > 1:
    print "There are messages in this thread"
    # loop through all past messages
    # check to see if message_id is in association table and then associate
    existing_association = Association.objects.get(thread_id=thread_id)
    for message in thread['messages']:
      existing_message = Association.objects.filter(email_id=message['id'])
      # if the message exists already, that means that it already associated
      if not existing_message:
        assocation = Association.objects.create(
            thread_id = thread_id,
            email_id = message['id'],
            opportunity = existing_association.opportunity,
            created_user = user
            )
        print "associated: %s" % assocation.id




  return HttpResponse(status=200) 
  
@csrf_exempt
def future(request):
  # create gmail service object
  # loop through and check all messages in threads
  thread_id = request.GET['thread_id']
  message_id = request.GET['message_id']
  
  
  existing_association = Association.objects.filter(thread_id=thread_id)
  if existing_association:
      existing_message = Association.objects.filter(email_id=message_id)
      # if the message exists already, that means that it already associated
      if not existing_message:
        assocation = Association.objects.create(
            thread_id = thread_id,
            email_id = message_id,
            opportunity = existing_association[0].opportunity,
            created_user = existing_association[0].created_user
            )
        print "associated: %s" % assocation.id




  return HttpResponse(status=200) 
  




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



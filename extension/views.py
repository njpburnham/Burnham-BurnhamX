from django.shortcuts import render_to_response, get_object_or_404, redirect
from extension.models import Opportunity, Association
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from google.appengine.api import users


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
    if curr_assoc.count() > 0:
      variables['association'] = curr_assoc[0]
      return render_to_response("extension/already_associated.html", variables, context_instance=RequestContext(request))
    
    opps = Opportunity.objects.all()
    variables['opps'] = opps
    return render_to_response("extension/associate.html", variables, context_instance=RequestContext(request))
  else:
    variables = {}
    curr_opp = Opportunity.objects.get(pk=request.POST['opp'])
    # Just a single association
    
    association = Association()
    association.thread_id = thread_id
    association.email_id = message_id
    association.opportunity = curr_opp
    association.created_user = users.get_current_user()
    association.save()

    return redirect("/extension/thanks")

def thanks(request):
  return  render_to_response("extension/thanks.html")


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










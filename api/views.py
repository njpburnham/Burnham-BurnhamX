from rest_framework import viewsets, status
from api.serializers import OpportunitySerializer, AssociationSerializer, UsersSerializer, PermissionsSerializer
from extension.models import Opportunity, Association, Users
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, BulkModelViewSet
from google.appengine.api import users
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, date
from dateutil import parser


class OpportunityViewSet(BulkModelViewSet):
  queryset = Opportunity.objects.all()
  serializer_class = OpportunitySerializer
  
  def get_queryset(self):
    queryset = Opportunity.objects.all()
    name = self.request.QUERY_PARAMS.get("name", None)
    user = users.get_current_user()
    if name:
      # case insensitive search
      queryset = queryset.filter(name__istartswith=name)
    if user and name:
      queryset = queryset.filter(name__istartswith=name, users__email=user)
    return queryset


class AssociationViewSet(BulkModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer

    def get_queryset(self):
      queryset = Association.objects.all()
      thread_id = self.request.QUERY_PARAMS.get("thread_id", None)
      search = self.request.QUERY_PARAMS.get("search", None)
      since_date = self.request.QUERY_PARAMS.get("since", None)
      is_active = self.request.QUERY_PARAMS.get("active", None)
      message_id = self.request.QUERY_PARAMS.get('message_id', None)
      if message_id:
        queryset = queryset.filter(email_id=message_id)
      if thread_id:
        queryset = queryset.filter(thread_id=thread_id)
      if thread_id and is_active:
        if is_active == "true":
          queryset = queryset.filter(thread_id=thread_id, is_active=True)
        else:
          queryset = queryset.filter(thread_id=thread_id, is_active=False)
      if since_date:
        since = parser.parse(since_date)
        queryset = queryset.filter(create_date__gt=since)
      if search:
        queryset = queryset.filter(Q(opportunity__siebel_id=search) | Q(opportunity__name__istartswith=search))

      return queryset


    def create(self, request):
      delete  = self.request.data.get("delete", None)
      message_id = self.request.data.get("messageID", None)

      if delete and message_id:
        assoc = Association.objects.filter(email_id=message_id)
        if not assoc:
          return  Response({"status":"Found no association with the message id of %s" % message_id}, status=status.HTTP_202_ACCEPTED)
        else:
          association = assoc[0]
          association.delete()
          return Response({"status":"Delete association with message id of %s" % message_id}, status=status.HTTP_200_OK)

      else:
        association = Association()
        association.email_id = self.request.data.get("email_id", None)
        association.thread_id = self.request.data.get("thread_id", None)
        if self.request.data.get('siebel_id'):
          opp = Opportunity.objects.get(siebel_id=self.request.data.get('siebel_id'))
          association.opportunity = opp
        else:
          association.opportunity_id = self.request.data.get("opportunity", None)
        association.created_user = self.request.data.get("created_user", None)
        association.is_active = True
        association.save()

        return Response({"status":"Created"}, status=status.HTTP_201_CREATED)


        
      
      

class UsersViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UsersSerializer


class PermissionsViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = PermissionsSerializer

  def create(self, request):
    user_email  = self.request.data.get("email", None)
    siebel_id = self.request.data.get("siebelID", None)
    delete = self.request.data.get("delete", None)
    
    # We're deleting objects here
    if delete:
      user = Users.objects.get(email=user_email)
      opp = Opportunity.objects.get(siebel_id=siebel_id)

      user.opportunities.remove(opp)

      return Response({"status":"deleted"}, status=status.HTTP_200_OK)
    else:
      return Resonse({"status":"error"})

    # we're creating objects here
    if user_email and siebel_id:
      #searializer = PermissionsSerializer(data={email=user_email})
      user = Users.objects.get(email=user_email)
      opp = Opportunity.objects.get(siebel_id=siebel_id)

      user.opportunities.add(opp)

      return Response({"status":"created"}, status=status.HTTP_201_CREATED)
    else:
      return Resonse({"status":"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

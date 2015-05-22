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
      is_active = self.request.QUERY_PARAMS.get("archive", None)
      if thread_id:
        queryset = queryset.filter(thread_id=thread_id)
      if since_date:
        since = parser.parse(since_date)
        print since
        queryset = queryset.filter(create_date__gt=since)
      if search:
        queryset = queryset.filter(Q(opportunity__siebel_id=search) | Q(opportunity__name__istartswith=search))

      return queryset

class UsersViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UsersSerializer


class PermissionsViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = PermissionsSerializer

  def create(self, request):
    user_email  = self.request.data.get("email", None)
    siebel_id = self.request.data.get("siebelID", None)
    
    if user_email and siebel_id:
      #searializer = PermissionsSerializer(data={email=user_email})
      user = Users.objects.get(email=user_email)
      opp = Opportunity.objects.get(siebel_id=siebel_id)

      user.opportunities.add(opp)

      return Response({"status":"created"}, status=status.HTTP_201_CREATED)
    else:
      return Resonse()

  def delete(self, request):
    user_email  = self.request.data.get("email", None)
    siebel_id = self.request.data.get("siebelID", None)
    
    if user_email and siebel_id:
      #searializer = PermissionsSerializer(data={email=user_email})
      user = Users.objects.get(email=user_email)
      opp = Opportunity.objects.get(siebel_id=siebel_id)

      user.opportunities.remove(opp)

      return Response({"status":"deleted"}, status=status.HTTP_201_CREATED)
    else:
      return Resonse()



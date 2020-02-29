from rest_framework import viewsets
from api.serializers import OpportunitySerializer, AssociationSerializer, UsersSerializer, PermissionsSerializer
from extension.models import Opportunity, Association, Users
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, BulkModelViewSet
from google.appengine.api import users
from rest_framework.response import Response


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
        queryset = queryset.filter(name__istartswith=name).filter(users__email=user)
      return queryset


class AssociationViewSet(BulkModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer

    def get_queryset(self):
      queryset = Association.objects.all()
      thread_id = self.request.QUERY_PARAMS.get("thread_id", None)
      if thread_id:
        queryset = queryset.filter(thread_id=thread_id)
      return queryset


class UsersViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UsersSerializer


#d0de5a3282b98955e158911efef5a8c16ec81607

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
      return Response()

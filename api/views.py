from rest_framework import viewsets, status
from api.serializers import OpportunitySerializer, AssociationSerializer, UsersSerializer, PermissionsSerializer
from extension.models import Opportunity, Association, Users
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, BulkModelViewSet
from google.appengine.api import users, memcache
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, date
from dateutil import parser
from django.core.cache import cache
import logging

class OpportunityViewSet(BulkModelViewSet):
  queryset = Opportunity.objects.all()
  serializer_class = OpportunitySerializer

  def get_queryset(self):
    queryset = Opportunity.objects.all()
    name = self.request.QUERY_PARAMS.get("name", None)
    user = users.get_current_user()
    limit = self.request.QUERY_PARAMS.get("limit", None)
    if name:
      # case insensitive search
      queryset = queryset.filter(name__istartswith=name)
    if user and name:
      queryset = queryset.filter(name__istartswith=name, users__email=user)
    if limit:
      return queryset[:10]
    else:
      return queryset

  def create(self, request):
    name = self.request.data.get("name", None)
    opp_status = self.request.data.get("status", None)
    street = self.request.data.get("street", None)
    city = self.request.data.get("city", None)
    state = self.request.data.get("state", None)
    zip_code = self.request.data.get("zip_code", None)
    siebel_id = self.request.data.get("siebel_id", None)

    opp_exists = Opportunity.objects.filter(siebel_id=siebel_id).exists()
    if opp_exists:
      # update
      opp = Opportunity.objects.filter(siebel_id=siebel_id)[0]
      opp.name = name
      opp.status = opp_status
      opp.street = street
      opp.city = city
      opp.state = state
      opp.zip_code = zip_code
      opp.siebel_id = siebel_id
      request_status = "Updated"
    else:
      # create
      opp = Opportunity()
      opp.name = name
      opp.status = opp_status
      opp.street = street
      opp.city = city
      opp.state = state
      opp.zip_code = zip_code
      opp.siebel_id = siebel_id
      request_status = "Created"
    opp.save()



    return Response({"status":request_status}, status=status.HTTP_201_CREATED)



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
      limit = self.request.QUERY_PARAMS.get("limit", None)
      # if not message_id and not thread_id:
      #   return Association.objects.none()

      if message_id:
        queryset = queryset.filter(email_id=message_id)
      if thread_id:
        data = cache.get("assoc_" + thread_id)
        if data:
          logging.info("cache")
          return data
        else:
          queryset = queryset.filter(thread_id=thread_id)
          logging.info("no cache")
          cache.set("assoc_" + thread_id, queryset)
          return queryset
      if thread_id and is_active:
        data = cache.get("active" + thread_id)
        if data:
          logging.info("cache")
          return data
        else:
          if is_active == "true":
            queryset = queryset.filter(thread_id=thread_id, is_active=True)
          else:
            queryset = queryset.filter(thread_id=thread_id, is_active=False)
          cache.set("active" + thread_id, queryset)

      if since_date:
        since = parser.parse(since_date)
        logging.info(since)
        queryset = queryset.filter(create_date__gt=since)
      if search:
        queryset = queryset.filter(Q(opportunity__siebel_id=search) | Q(opportunity__name__istartswith=search))

      if limit:
        return queryset[:limit]
      else:
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
          memcache.delete("assosc_" + association.thread_id)
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
        memcache.add("assosc_" + association.thread_id, "a")



        return Response({"status":"Created"}, status=status.HTTP_201_CREATED)






class UsersViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UsersSerializer


  def create(self, request):
    email = self.request.data.get('email', None)
    if email:
      user = Users.objects.filter(email=email)
      if user:
        user = user[0]
        user.email = email
        user.save()
        return Response({"status":"updated"}, status=status.HTTP_200_OK)
      else:
        user = Users()
        user.email = email
        user.save()
        return Response({"status":"created"}, status=status.HTTP_200_OK)


class PermissionsViewSet(BulkModelViewSet):
  queryset = Users.objects.all()
  serializer_class = PermissionsSerializer

  def create(self, request):
    user_email  = self.request.data.get("email", None)
    siebel_id = self.request.data.get("siebelID", None)
    delete = self.request.data.get("delete", None)

    # We're deleting objects here
    if delete:
      user = Users.objects.filter(email=user_email)
      if user:
        user = user[0]
        opp = Opportunity.objects.get(siebel_id=siebel_id)

        user.opportunities.remove(opp)

        return Response({"status":"deleted"}, status=status.HTTP_200_OK)

    if user_email and siebel_id:
      #searializer = PermissionsSerializer(data={email=user_email})
      if "burnham" in user_email:
        user = Users.objects.filter(email=user_email)
        if user:
          user = user[0]
          opp = Opportunity.objects.get(siebel_id=siebel_id)
          # Check if duplicate first
          if user.opportunities.filter(id=opp.id):
            return Response({"status":"already exists"}, status=status.HTTP_200_OK)
          else:
            user.opportunities.add(opp)
            return Response({"status":"created"}, status=status.HTTP_201_CREATED)
        else:
          return Response({"status":"error. User does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      else:
        return Response({"status":"error. Please provide a burnham email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      return Response({"status":"error. Please provide siebelID and email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
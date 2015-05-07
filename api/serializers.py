from rest_framework import serializers
from django.forms import widgets
from extension.models import Opportunity, Association, Users
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView

class OpportunitySerializer(BulkSerializerMixin, serializers.ModelSerializer):
  class Meta:
    model = Opportunity
    list_serializer_class = BulkListSerializer
    many = True
    depth = 1
    fields = ("name","status","street","city","state","zip_code","siebel_id","create_date","modified_date","id")


class AssociationSerializer(BulkSerializerMixin, serializers.ModelSerializer):
  opportunity = OpportunitySerializer()
  
  class Meta:
    model = Association
    list_serializer_class = BulkListSerializer

    
    
class UsersSerializer(BulkSerializerMixin, serializers.ModelSerializer):

  class Meta:
    model = Users
    list_serializer_class = BulkListSerializer


class PermissionsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
  
  class Meta:
    model = Users
    list_serializer_class = BulkListSerializer
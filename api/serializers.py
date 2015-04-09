from rest_framework import serializers
from django.forms import widgets
from extension.models import Opportunity, Association

class OpportunitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Opportunity


class AssociationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Association
    



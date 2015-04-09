from rest_framework import viewsets
from api.serializers import OpportunitySerializer, AssociationSerializer
from extension.models import Opportunity, Association

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer


class AssociationViewSet(viewsets.ModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer


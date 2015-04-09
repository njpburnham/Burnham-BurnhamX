from rest_framework import viewsets
from api.serializers import OpportunitySerializer, AssociationSerializer
from extension.models import Opportunity, Association
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, BulkModelViewSet

class OpportunityViewSet(BulkModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer



class AssociationViewSet(BulkModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer



#d0de5a3282b98955e158911efef5a8c16ec81607
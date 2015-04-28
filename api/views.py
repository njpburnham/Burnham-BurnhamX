from rest_framework import viewsets
from api.serializers import OpportunitySerializer, AssociationSerializer
from extension.models import Opportunity, Association
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, BulkModelViewSet

class OpportunityViewSet(BulkModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    
    def get_queryset(self):
      queryset = Opportunity.objects.all()
      name = self.request.QUERY_PARAMS.get("name", None)
      if name:
        # case insensitive search
        queryset = queryset.filter(name__istartswith=name)
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


#d0de5a3282b98955e158911efef5a8c16ec81607
import graphene
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from graphene_django_filter import AdvancedDjangoFilterConnectionField, AdvancedFilterSet
from ranq_app.models import Poll

class PollFilter(AdvancedFilterSet):
    class Meta:
        model = Poll
        fields = {
            'token': ('exact', 'icontains', 'istartswith'),
            'title': ('exact', 'icontains', 'istartswith'),
            'description': ('exact', 'icontains', 'istartswith'),
        }
        
class PollNode(DjangoObjectType):
    class Meta:
        model = Poll
        fields = "__all__"
        filterset_class = PollFilter
        interfaces = (graphene.relay.Node,)
        
        
        
        

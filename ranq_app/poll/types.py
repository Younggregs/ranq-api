import graphene
from graphene_django import DjangoObjectType
from ranq_app.models import Poll, Result

class PollType(DjangoObjectType):
    class Meta:
        model = Poll
        fields = '__all__'
    
class ResultType(DjangoObjectType):
    class Meta:
        model = Result
        fields = '__all__'
        
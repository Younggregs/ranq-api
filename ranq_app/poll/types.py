import graphene
from graphene_django import DjangoObjectType
from ranq_app.models import Poll, Result, Voter

class PollType(DjangoObjectType):
    class Meta:
        model = Poll
        fields = '__all__'
        
    # custom field
    votes = graphene.Int()
    result = graphene.Field('ranq_app.poll.types.ResultType')
    
    resolve_votes = lambda self, info: Voter.objects.filter(poll_id=self.id, voted=True).count()
    
    resolve_result = lambda self, info: Result.objects.get(poll_id=self.id)
    
class ResultType(DjangoObjectType):
    class Meta:
        model = Result
        fields = '__all__'
        
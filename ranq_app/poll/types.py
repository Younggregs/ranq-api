from graphene import relay
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
    voted = graphene.Boolean()
    
    resolve_votes = lambda self, info: Voter.objects.filter(poll_id=self.id, voted=True).count()
    
    resolve_result = lambda self, info: Result.objects.get(poll_id=self.id)
    
    resolve_voted = lambda self, info: Voter.objects.filter(poll_id=self.id, email=info.context.user.email).exists()
    
        
class ResultType(DjangoObjectType):
    class Meta:
        model = Result
        fields = '__all__'
        
class PollStatusType(graphene.ObjectType):
    is_valid = graphene.Boolean()
    poll_status = graphene.String()
    is_logged_in = graphene.Boolean()
    title = graphene.String()
    email = graphene.String()
    name = graphene.String()
    
class VoterType(DjangoObjectType):
    class Meta:
        model = Voter
        fields = '__all__'
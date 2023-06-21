from graphene_django import DjangoObjectType
from ranq_app.models import Vote, Voter

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = '__all__'
        
class VoterType(DjangoObjectType):
    class Meta:
        model = Voter
        fields = '__all__'
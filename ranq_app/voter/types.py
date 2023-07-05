import graphene
from graphene_django import DjangoObjectType
from ranq_app.models import Voter

class VoterType(DjangoObjectType):
    class Meta:
        model = Voter
        fields = ('id', 'email')
        

class VoterStatusType(graphene.ObjectType):
    is_valid = graphene.Boolean()
    is_logged_in = graphene.Boolean()
    poll_status = graphene.String()
    voted = graphene.Boolean()
    token = graphene.String()
    title = graphene.String()
    email = graphene.String()
    name = graphene.String()
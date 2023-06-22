from graphene_django import DjangoObjectType
from ranq_app.models import Voter

class VoterType(DjangoObjectType):
    class Meta:
        model = Voter
        fields = ('id', 'email')
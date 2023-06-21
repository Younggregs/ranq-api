from graphene_django import DjangoObjectType
from ranq_app.models import Poll

class PollType(DjangoObjectType):
    class Meta:
        model = Poll
        fields = '__all__'
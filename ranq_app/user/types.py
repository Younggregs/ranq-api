import graphene
from graphene_django import DjangoObjectType
from ranq_app.lib.random import Random
from ranq_app.models import User, EmailToken

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        
class EmailTokenType(DjangoObjectType):
    
    class Meta:
        model = EmailToken
        fields = ('email', 'type')
        
    # custom field
    is_returning = graphene.Boolean()
    raw_token = graphene.String()
    name = graphene.String()
    
    resolve_is_returning = lambda self, info: User.objects.filter(email=self.email).exists()
    
    resolve_raw_token = lambda self, info: Random.generate_random_string(16)
    
    resolve_name = lambda self, info: User.objects.get(email=self.email).first_name
    
        
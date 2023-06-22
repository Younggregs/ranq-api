from graphene_django import DjangoObjectType
from ranq_app.models import User, EmailToken

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        
class EmailTokenType(DjangoObjectType):
    
    class Meta:
        model = EmailToken
        fields = ('email', 'type')
        
import graphene
from ranq_app.models import User
from ranq_app.user.types import UserType
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class SignupMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, name, email, password):
        # raw_password = password
        
        user = get_user_model()(
            first_name=name,
            email=email,
        )
        user.set_password(password)
        user.save()
        
        # Notice we return an instance of this mutation
        return SignupMutation(user=user)
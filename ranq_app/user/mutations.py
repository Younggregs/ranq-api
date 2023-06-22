import graphene
from ranq_app.models import User, EmailToken
from ranq_app.user.types import UserType, EmailTokenType
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from ranq_app.lib.random import Random
from ranq_app.lib.email import Email


class EmailVerificationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        type = graphene.String(required=True)

    # The class attributes define the response of the mutation
    emailToken = graphene.Field(EmailTokenType)

    @classmethod
    def mutate(cls, root, info, email, type):
        # raw_password = password
        
        templateId = 1
        page = "signup"
        if type == 'signup_email':
            pass
        elif type == 'vote_email':
            templateId = 2
        elif type == 'forgot_password_email':
            templateId = 3
        else:
            pass
        
        token = Random.generate_random_string()
        newEmail = Email(email, token, page, templateId)
        try:
            newEmail.send()
        except:
            pass
        
        emailToken = ""
        if EmailToken.objects.filter(email=email).exists():
            emailToken = EmailToken.objects.get(email=email)
        else:
             emailToken = EmailToken()
             emailToken.email = email
        
        emailToken.type = type
        emailToken.token = token
        emailToken.save()
        
        # Notice we return an instance of this mutation
        return EmailVerificationMutation(emailToken=emailToken)

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
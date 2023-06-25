import graphene
from ranq_app.models import User, EmailToken
from ranq_app.types import ErrorType
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
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, email, type):
        # raw_password = password
        
        templateId = 1
        name = ""
        page = "signin"
        if type == 'signup_email':
            pass
        elif type == 'forgot_password_email':
            templateId = 4
            page = "reset-password"
            user = User.objects.get(email=email)
            name = user.first_name
        else:
            pass
        
        
        token = Random.generate_random_string()
        
        emailToken = ""
        if EmailToken.objects.filter(email=email).exists():
            emailToken = EmailToken.objects.get(email=email)
        else:
             emailToken = EmailToken()
             emailToken.email = email
        
        emailToken.type = type
        emailToken.token = token
        emailToken.save()
        
        try: 
            Email.send(email, token, page, templateId, "", name)
        except:
            pass
        
        # Notice we return an instance of this mutation
        return EmailVerificationMutation(success=True, errors=None, emailToken=emailToken)

class SignupMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, name, email, password):
        # raw_password = password
        
        # check if email is valid
        if not EmailToken.objects.filter(email=email, type="signup_email").exists():
            return SignupMutation(success=False, errors=ErrorType(message='Email has not been verified'), user=None)
        
        # check if email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            user = get_user_model()(
                first_name=name,
                email=email,
            )

        user.set_password(password)
        user.save()
        
        # Notice we return an instance of this mutation
        return SignupMutation(success=True, errors=None, user=user)
    
    

class ResetPasswordMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        password = graphene.String(required=True)
        token = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, token, password):
       
        try:
            emailToken = EmailToken.objects.get(token=token)
            user = User.objects.get(email=emailToken.email)
            user.set_password(password)
            user.save()
        except:
            return ResetPasswordMutation(success=False, errors=ErrorType(message='Invalid token'), user=None)
        
        return ResetPasswordMutation(success=True, errors=None, user=user)
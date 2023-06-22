import graphene
from ranq_app.models import User, Poll, EmailToken
from ranq_app.user.types import UserType, EmailTokenType
from ranq_app.poll.types import PollType

class Query(graphene.ObjectType):
    user_by_id = graphene.Field(UserType, id=graphene.String())
    users = graphene.List(UserType)
    poll_by_id = graphene.Field(PollType, id=graphene.String())
    polls = graphene.List(PollType)
    verify_email_token = graphene.Field(EmailTokenType, token=graphene.String(), type=graphene.String())
    
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_question_by_id(root, info, id):
        return User.objects.get(pk=id)
    
    def resolve_polls(root, info, **kwargs):
        return Poll.objects.all()

    def resolve_poll_by_id(root, info, id):
        return Poll.objects.get(pk=id)
    
    def resolve_verify_email_token(root, info, token, type):
        try:
            return EmailToken.objects.get(token=token, type=type)
        except:
            pass
        return EmailToken.objects.none()
        
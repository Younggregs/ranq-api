import graphene
from ranq_app.models import User, Poll
from ranq_app.user.types import UserType
from ranq_app.poll.types import PollType

class Query(graphene.ObjectType):
    user_by_id = graphene.Field(UserType, id=graphene.String())
    users = graphene.List(UserType)
    poll_by_id = graphene.Field(PollType, id=graphene.String())
    polls = graphene.List(PollType)
    
    def resolve_users(root, info, **kwargs):
        # Querying a list
        return User.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return User.objects.get(pk=id)
    
    def resolve_polls(root, info, **kwargs):
        # Querying a list
        return Poll.objects.all()

    def resolve_poll_by_id(root, info, id):
        # Querying a single question
        return Poll.objects.get(pk=id)
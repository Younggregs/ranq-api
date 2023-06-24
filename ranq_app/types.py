import graphene
from ranq_app.poll.types import PollType

class ErrorType(graphene.ObjectType):
    message = graphene.String()
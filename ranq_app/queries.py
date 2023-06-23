import graphene
from ranq_app.models import Result, User, Poll, EmailToken, Voter
from ranq_app.user.types import UserType, EmailTokenType
from ranq_app.poll.types import PollType, ResultType

class Query(graphene.ObjectType):
    user_by_id = graphene.Field(UserType, id=graphene.String())
    users = graphene.List(UserType)
    poll_by_id = graphene.Field(PollType, id=graphene.String())
    polls = graphene.List(PollType)
    verify_email_token = graphene.Field(EmailTokenType, token=graphene.String(), type=graphene.String())
    fetch_rank_poll = graphene.Field(PollType, token=graphene.String())
    poll_result = graphene.Field(ResultType, token=graphene.String())
    
    def resolve_users(root, info, **kwargs):
        return User.objects.all()
    
    def resolve_polls(root, info, **kwargs):
        return Poll.objects.all()

    def resolve_poll_by_id(root, info, id):
        return Poll.objects.get(token=id)
    
    def resolve_verify_email_token(root, info, token, type):
        try:
            return EmailToken.objects.get(token=token, type=type)
        except:
            pass
        return EmailToken.objects.none()
    
    def resolve_fetch_rank_poll(root, info, token):
        # check if token is valid
        if not Voter.objects.filter(token=token).exists():
            return Poll.objects.none()
        
        # check if user has voted
        if Voter.objects.get(token=token).voted:
            return Poll.objects.none()
        
        voter = Voter.objects.get(token=token)
        return Poll.objects.get(id=voter.poll_id.id)
    

    def resolve_poll_result(root, info, token):
        # check if token is valid or ongoing
        if not Poll.objects.filter(token=token).exists() or Poll.objects.get(token=token).status == "ongoing":
            return Poll.objects.none()
        
        # get result
        poll = Poll.objects.get(token=token)
        return Result.objects.get(poll_id=poll)
        
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_filter import AdvancedDjangoFilterConnectionField, AdvancedFilterSet
from ranq_app.models import Result, TypeEnum, User, Poll, EmailToken, Vote, Voter
from ranq_app.poll.relay import PollNode
from ranq_app.result.popular_vote import PopularVote
from ranq_app.result.ranq_bar import RanqBar
from ranq_app.user.types import UserType, EmailTokenType
from ranq_app.poll.types import PollStatusType, PollType, ResultType, VoterType
from ranq_app.voter.types import VoterStatusType

class Query(graphene.ObjectType):
    user_by_id = graphene.Field(UserType, id=graphene.String())
    users = graphene.List(UserType)
    poll_by_id = graphene.Field(PollType, id=graphene.String())
    calculate_result = graphene.Field(PollType, token=graphene.String()) 
    voters = graphene.List(VoterType, id=graphene.String())
    polls = AdvancedDjangoFilterConnectionField(PollNode)
    public_polls = AdvancedDjangoFilterConnectionField(PollNode)
    verify_email_token = graphene.Field(EmailTokenType, token=graphene.String(), type=graphene.String())
    poll_status = graphene.Field(PollStatusType, token=graphene.String())
    voter_status = graphene.Field(VoterStatusType, token=graphene.String())
    fetch_rank_poll = graphene.Field(PollType, token=graphene.String())
    poll_result = graphene.Field(ResultType, token=graphene.String())
    
    def resolve_users(root, info, **kwargs):
        return User.objects.all()
    
    def resolve_polls(root, info, **kwargs):
        # check if user is logged in
        user = info.context.user
        if user.is_authenticated:
            poll = Poll.objects.filter(created_by=user)
            return poll
        return Poll.objects.none()

    def resolve_voters(root, info, id):
        return Voter.objects.filter(poll_id=id)

    def resolve_calculate_result(root, info, token):
        #1. get poll contestants array, and create a dictionary of contestants 
        # with their name as key and index as value
        #2. get all voters for the poll
        #3. for each voter, get votes
        #4. create a dictionary of votes with contestant index as key and rank as value
        #5. compare the poll contestants dict with the voter dict
        #6. if thesame, add to list, else pass
        
        poll = Poll.objects.get(token=token)
        n = len(poll.contestants)
        poll_contestants = {v: n - k for k, v in enumerate(poll.contestants)}
        
        voters = Voter.objects.filter(poll_id=poll)
        valid_voters = []
        for voter in voters:
            voter_votes = Vote.objects.filter(voter_id=voter, poll_id=poll)
            voter_votes_dict = {k.contestant_id.name: k.rank_value for k in voter_votes}
            
            if poll_contestants != voter_votes_dict:
                valid_voters.append(voter.id)
        
        if Result.objects.filter(poll_id=poll).exists():
            result = Result.objects.get(poll_id=poll)
        else:
            result = Result()
            result.poll_id = poll
        result.popular_vote = PopularVote.rank(poll.id, valid_voters)
        result.rank_raise_bar = str(valid_voters)
        result.save()
        return poll
    
    def resolve_public_polls(root, info, **kwargs):
        return Poll.objects.filter(type = TypeEnum.public.value)
    
    def resolve_poll_by_id(root, info, id):
        return Poll.objects.get(token=id)
    
    def resolve_verify_email_token(root, info, token, type):
        try:
            return EmailToken.objects.get(token=token, type=type)
        except:
            pass
        return EmailToken.objects.none()
    
    def resolve_poll_status(root, info, token):
        
        is_valid = False
        poll_status = "ongoing"
        is_logged_in = False
        title = ""
        email = ""
        name = ""
        # check if token is valid
        if Poll.objects.filter(token=token).exists():
            is_valid = True
            
            # check if poll has ended
            if Poll.objects.filter(token=token, status="completed").exists():
                poll_status = "completed"
            
            # check if user is logged in
            user = info.context.user
            if user.is_authenticated:
                is_logged_in = True
                email = user.email
                name = user.first_name
            
            # poll data
            title = Poll.objects.get(token=token).title
            
        return PollStatusType(is_valid=is_valid, poll_status=poll_status, is_logged_in=is_logged_in, title=title, email=email, name=name)
            
    
    def resolve_voter_status(root, info, token):
        
        is_valid = False
        poll_status = "ongoing"
        is_logged_in = False
        voted = False
        title = ""
        name = ""
        email = ""
        
        # check if user is logged in
        user = info.context.user
        if user.is_authenticated:
            is_logged_in = True
            email = user.email
            name = user.first_name
        
        # check if token is valid
        if Poll.objects.filter(token=token).exists():
            poll = Poll.objects.get(token=token)
            title = poll.title
            is_valid = True
            if poll.status == "completed":
                    poll_status = "completed"
            
            if Voter.objects.filter(email=email, poll_id=poll).exists():
                voter = Voter.objects.get(email=email, poll_id=poll)
                
                # check if voter has voted
                if voter.voted:
                    voted = True
            
        return VoterStatusType(is_valid=is_valid, poll_status=poll_status, voted=voted, token=token, title=title, is_logged_in=is_logged_in, name = name, email=email)
    
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
        
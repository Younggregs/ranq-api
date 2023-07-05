import graphene
from ranq_app.lib.random import Random
from ranq_app.models import Vote, Voter, Poll, Contestant
from ranq_app.poll.types import PollType
from ranq_app.types import ErrorType

class CreateVoteMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String(required=True)
        ranked = graphene.List(graphene.String)


    # The class attributes define the response of the mutation
    poll = graphene.Field(PollType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id, ranked):
        
        # check if user is logged in
        user = info.context.user
        if user.is_authenticated:
            email = user.email
        else:
            return CreateVoteMutation(success=False, errors=ErrorType(message='Sigin needed to complete this action'), poll=None)
        
        # check if voter has voted
        if Voter.objects.filter(poll_id=id, email=email, voted=True).exists():
            return CreateVoteMutation(success=False, errors=ErrorType(message='This vote link have been used already'), poll=None)
    
        poll = Poll.objects.get(id=id)
     
        voter = Voter()
        voter.poll_id = poll
        voter.email = email
        voter.token = Random.generate_random_string()
        voter.save()
        
        # check if poll has ended
        if poll.status == "completed":
            CreateVoteMutation(success=False, errors=ErrorType(message='Poll has ended'), poll=None)
        
        # reverse list so the first get the highest rank
        ranked.reverse()
        for item in ranked:
            vote = Vote()
            vote.voter_id = voter
            vote.poll_id = poll
            vote.contestant_id = Contestant.objects.get(name=item, poll_id=poll)
            vote.rank_value = ranked.index(item) + 1
            vote.save()
            
        voter.voted = True
        voter.save()
            
        
        return CreateVoteMutation(success=False, errors=None, poll=poll)
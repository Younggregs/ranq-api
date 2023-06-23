import graphene
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

    @classmethod
    def mutate(cls, root, info, id, ranked):
        
        # check if voter has voted
        if Voter.objects.filter(token=id, voted=True).exists():
            return CreateVoteMutation.objects.none()
        voter = Voter.objects.get(token=id)
        poll = Poll.objects.get(id=voter.poll_id.id)
        
        voter = Voter.objects.get(token=id)
        poll = Poll.objects.get(id=voter.poll_id.id)
        
        # check if poll has ended
        if poll.status == "completed":
            return CreateVoteMutation.objects.none()
        
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
            
        
        return CreateVoteMutation(poll=poll)
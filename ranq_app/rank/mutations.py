import graphene
from ranq_app.models import Vote, Voter, Poll, Contestant
from ranq_app.poll.types import PollType

class CreateVoteMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String(required=True)
        ranked = graphene.List(graphene.String)


    # The class attributes define the response of the mutation
    poll = graphene.Field(PollType)

    @classmethod
    def mutate(cls, root, info, id, ranked):
        
        poll = Poll.objects.get(id=id)
        
        voter = 1
        if Voter.objects.filter(email='anonymous@gmail.com').exists():
            voter = Voter.objects.get(email='anonymous@gmail.com')
        else:
            voter = Voter()
            voter.email = 'anonymous@gmail.com'
            voter.save()
        
        # reverse list so the first get the highest rank
        ranked.reverse()
        for item in ranked:
            vote = Vote()
            vote.voter_id = voter
            vote.poll_id = poll
            vote.contestant_id = Contestant.objects.get(name=item, poll_id=id)
            vote.rank_value = ranked.index(item) + 1
            vote.save()
            
        
        return CreateVoteMutation(poll=poll)
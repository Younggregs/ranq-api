import graphene
from ranq_app.models import Poll, Contestant
from ranq_app.poll.types import PollType

class CreatePollMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        contestants = graphene.List(graphene.String)
        type = graphene.String(required=True)
        voters = graphene.List(graphene.String)
        duration = graphene.String(required=True)


    # The class attributes define the response of the mutation
    poll = graphene.Field(PollType)

    @classmethod
    def mutate(cls, root, info, title, description, contestants, type, voters, duration):
        user = info.context.user
        if not user.is_authenticated:
            return Poll.objects.none()
        
        poll = Poll()
        poll.created_by = user
        poll.title = title
        poll.description = description
        poll.contestants = contestants
        poll.type = type
        poll.voters = voters
        poll.duration = duration
        poll.save()
        
        # save contestants
        for item in contestants:
            contestant = Contestant()
            contestant.poll_id = poll
            contestant.name = item
            contestant.save()
            
        
        return CreatePollMutation(poll=poll)
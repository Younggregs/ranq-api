import graphene
from ranq_app.models import Poll, Contestant, PrivateVoter, Voter
from ranq_app.poll.types import PollType
from ranq_app.lib.email import Email
from ranq_app.lib.random import Random
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
        poll.token = Random.generate_random_string(6)
        poll.save()
        
        # save contestants
        for item in contestants:
            contestant = Contestant()
            contestant.poll_id = poll
            contestant.name = item
            contestant.save()
            
        # save private voters
        if type.lower() == 'private':
            for email in voters:
                voter = PrivateVoter()
                voter.poll_id = poll
                voter.email = email
                voter.save()
                
                token = Random.generate_random_string()
                voter = Voter()
                voter.poll_id = poll
                voter.email = email
                voter.token = token
                voter.save()
                
                # send email
                newEmail = Email(email, token, 'rank', 2)
                try:
                    newEmail.send()
                except:
                    pass
                
        
        return CreatePollMutation(poll=poll)
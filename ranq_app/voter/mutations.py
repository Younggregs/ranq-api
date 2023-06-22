import graphene
from ranq_app.models import Vote, Voter, Poll, Contestant
from ranq_app.voter.types import VoterType
from ranq_app.lib.random import Random
from ranq_app.lib.email import Email
from ranq_app.types import ErrorType

class CreateVoterMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        token = graphene.String(required=True)
        email = graphene.String(required=True)

    # The class attributes define the response of the mutation
    voter = graphene.Field(VoterType)
    error = graphene.Field(ErrorType)

    @classmethod
    def mutate(cls, root, info, token, email):
        
        # check if token is valid
        if not Poll.objects.filter(token=token).exists():
            return CreateVoterMutation(error=ErrorType(message='Invalid token'))
        
        # check if user has voted
        if Voter.objects.filter(email=email, poll_id=Poll.objects.get(token=token), voted=True).exists():
            return CreateVoterMutation(error=ErrorType(message='This email already voted'))
        
        # check if user email is registered as voter
        voter = ""
        if Voter.objects.filter(email=email, poll_id=Poll.objects.get(token=token)).exists():
            voter = Voter.objects.get(email=email, poll_id=Poll.objects.get(token=token))
        else:
            # create voter
            voter = Voter()
            voter.poll_id = Poll.objects.get(token=token)
            voter.email = email
        
        voterToken = Random.generate_random_string()
        voter.token = voterToken
        voter.save()
        
        newEmail = Email(email, voterToken, 'rank', 2)
        try:
            newEmail.send()
        except:
            pass

        return CreateVoterMutation(voter=voter)
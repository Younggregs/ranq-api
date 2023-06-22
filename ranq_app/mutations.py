import graphene
import graphql_jwt
from ranq_app.user.mutations import SignupMutation, EmailVerificationMutation
from ranq_app.poll.mutations import CreatePollMutation
from ranq_app.rank.mutations import CreateVoteMutation

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    email_verification = EmailVerificationMutation.Field()
    signup = SignupMutation.Field()
    create_poll = CreatePollMutation.Field()
    create_vote = CreateVoteMutation.Field()
    
    
import graphene
import graphql_jwt
from ranq_app.user.mutations import SignupMutation
from ranq_app.poll.mutations import CreatePollMutation

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    signup = SignupMutation.Field()
    create_poll = CreatePollMutation.Field()
    
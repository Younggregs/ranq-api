import graphene
from ranq_app.mutations import Mutation
from ranq_app.queries import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
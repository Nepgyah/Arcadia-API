import graphene

# Define a set of inputs for graphene
class MediaSortInput(graphene.InputObjectType):
    category = graphene.String()
    direction = graphene.String()

class PaginationInput(graphene.InputObjectType):
    per_page = graphene.Int()
    target_page = graphene.Int()

class PaginationResults(graphene.ObjectType):
    per_page = graphene.Int()
    total_pages = graphene.Int()
    total_items = graphene.Int()
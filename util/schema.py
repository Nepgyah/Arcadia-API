from graphene import (
    InputObjectType,
    String,
    Int
)
# Define a set of inputs for graphene
class MediaSortInput(InputObjectType):
    category = String()
    direction = String()

class PaginationInput(InputObjectType):
    per_page = Int()
    current_page = Int()
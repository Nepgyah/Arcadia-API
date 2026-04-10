import graphene

class TokenType(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()
    httponly = graphene.Boolean()
    secure = graphene.Boolean()
    samesite = graphene.String()
    expires = graphene.String()
    path = graphene.String()
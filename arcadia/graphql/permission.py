import typing
import strawberry
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):

    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs):
        profile_id = getattr(info.context, 'user_id', None)
        if profile_id is None:
            #TODO: Reintroduce account exceptions
            pass
            # raise NotLoggedInError()
        
        return True
import typing
import strawberry
from strawberry.permission import BasePermission
from authorization.exceptions import NotLoggedInError

class IsAuthenticated(BasePermission):

    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs):
        user_id = getattr(info.context, 'user_id', None)
        if user_id is None:
            raise NotLoggedInError()
        
        return True
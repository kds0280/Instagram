from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserMineOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.id == obj.id
        )

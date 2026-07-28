from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsTaskOwnerOrCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (obj.project.owner == request.user or obj.created_by == request.user)


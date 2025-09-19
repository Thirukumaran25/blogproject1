from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any request.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user

class IsAuthenticatedAndCreate(permissions.BasePermission):
    """
    Custom permission to allow authenticated users to create an object,
    but only allow the owner to edit or delete it.
    Read-only permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Allow any authenticated user to create a new object (POST).
        if view.action == 'create':
            return request.user and request.user.is_authenticated
        
        # For other actions, defer to has_object_permission.
        return True

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user

class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to read. Write actions require either admin user or object owner.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return getattr(obj, 'author', None) == request.user
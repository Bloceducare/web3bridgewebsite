from ... import permissions
class GuestReadAllWriteAdminOnlyPermissionMixin:
    admin_actions = []
    
    def get_permissions(self):
        if self.action in self.admin_actions:
            return super().get_permissions() + [permissions.IsAuthenticatedByAuthServer()]
        return []
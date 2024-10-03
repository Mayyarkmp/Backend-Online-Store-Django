from django.contrib.contenttypes.models import ContentType
from permissions.models import AssignedBranches, Role, Permission
from branches.models import Branch  # Assuming you have a Branch model


class BranchDataFetcher:
    def __init__(self, user, model):
        self.user = user
        self.model = model
        self.content_type = ContentType.objects.get_for_model(model)

    def fetch_data(self):
        
        if self.user.is_superuser:
            return self.model.objects.all()

        permissions = self.user.permissions.filter(content_type=self.content_type).first()

        if not permissions:
            return self.model.objects.none()

        if permissions.level == Permission.Levels.ALL:
            return self.model.objects.all()

        if permissions.level == Permission.Levels.ASSIGNED_BRANCHES:
            return self._fetch_assigned_branches_data()

        if permissions.level == Permission.Levels.OWNER:
            return self._fetch_owner_branch_data()

        return self.model.objects.none()

    def _fetch_assigned_branches_data(self):
        try:
            assigned_branches = AssignedBranches.objects.get(user=self.user)
            return self.model.objects.filter(branch__in=assigned_branches.branches.all())
        except AssignedBranches.DoesNotExist:
            return self.model.objects.none()

    def _fetch_owner_branch_data(self):
        try:
            branch = Branch.objects.get(owner=self.user)
            return self.model.objects.filter(branch=branch)
        except Branch.DoesNotExist:
            return self.model.objects.none()

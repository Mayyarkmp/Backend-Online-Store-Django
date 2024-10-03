from users.models import User
from users.base.models import UserManager

class AdminManager(UserManager):
    def create_user(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        if not branch:
            return ValueError('No branch provided')
        user = self.model(*args, **kwargs)
        user.set_for_branch(job=user.BranchJobs.ADMIN)
        user.status = user.Status.REVIEWING
        user.save()
        return user

class Admin(User):
    objects = AdminManager()
    class Meta:
        proxy = True


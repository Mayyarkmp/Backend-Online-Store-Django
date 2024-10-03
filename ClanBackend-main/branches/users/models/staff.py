from users.models import User
from users.base.models import UserManager



class StaffManager(UserManager):
    def create_user(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        if not branch:
            return ValueError('No branch provided')
        user = self.model(*args, **kwargs)
        user.set_for_branch(job=user.BranchJobs.STAFF)
        user.status = user.Status.REVIEWING
        user.save()
        return user


class Staff(User):
    objects = StaffManager()
    class Meta:
        proxy = True

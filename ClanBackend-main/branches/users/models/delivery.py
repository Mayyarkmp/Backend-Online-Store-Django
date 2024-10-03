from users.models import User
from users.base.models import UserManager


class DeliveryManager(UserManager):

    def create_user(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        if not branch:
            return ValueError('No branch provided')

        user = self.model(*args, **kwargs)
        user.set_for_branch(job=user.BranchJobs.DELIVERY)
        user.status = user.Status.REVIEWING
        user.save()

class Delivery(User):
    objects = DeliveryManager()
    class Meta:
        proxy = True
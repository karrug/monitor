import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.username


class Screenshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete='CASCADE')

    def __str__(self):
        return '%s: %s' % (self.user, self.time)

    def get_name(self):
        return self.pk.hex

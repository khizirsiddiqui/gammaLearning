from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    message = models.CharField(default='', max_length=100)
    read = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=1)
    link = models.CharField(default='', blank=True, max_length=100)
    fa_type = models.TextField(default='fa-star')

    def mark_as_read(self):
        self.read = True
        self.save()
        return True

    def to_dict(self):
        values = {'message': self.message, 'read': self.read,
                  'fa_type': self.fa_type, 'link': self.link}
        return values

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.user.username + '-' + self.message

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MemberQuerySet(models.QuerySet):

    def _get_member(self, discord_user):
        member, created = self.get_or_create(discord_id=discord_user.id, defaults={'name': discord_user.name})
        if member.name != discord_user.name:
            member.name = discord_user.name
            member.save()
        return member, created

    def from_message(self, message):
        return self._get_member(message.author)[0]

    def from_mentions(self, mentions):
        return [self._get_member(member) for member in mentions]


class Member(models.Model):
    discord_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=255)

    can_admin_bot = models.BooleanField(default=False)

    objects = MemberQuerySet.as_manager()

    def __str__(self):
        return '<@{}>'.format(self.discord_id)

from django.db import models

from apps.enums import ExpirationDays
from .backends import AccessToken


class JwtToken(models.Model):
    expiration = models.SmallIntegerField(
        choices=ExpirationDays.choices, help_text='თოქენის ვალიდურობის დრო'
    )
    token = models.TextField(
        help_text='თოქენი დაგენერირდება ავტომატურად შენახვის შემდეგ'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tokens'
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, **kwargs):
        if not self.token and self.expiration:
            access_token = AccessToken(lifetime=self.expiration)
            self.token = str(access_token)
        super().save(**kwargs)

    def __str__(self):
        return self.token

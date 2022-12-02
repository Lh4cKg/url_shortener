from django.utils import timezone
from django.db import models


class Url(models.Model):
    redirect_url = models.TextField()
    url_key = models.CharField(max_length=30, db_index=True)
    usage_count = models.IntegerField(default=0)
    key = models.CharField(max_length=256, null=True, blank=True)
    tag = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'urls'
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'
        unique_together = (
            ('key', 'tag')
        )

    def __str__(self):
        return f'<Url(short_url={self.url_key}, usage_count={self.usage_count})>'

    def __repr__(self):
        return str(self)

    def is_expired(self):
        if self.expired:
            return timezone.now() > self.expired
        return False

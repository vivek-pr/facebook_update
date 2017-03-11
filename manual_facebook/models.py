from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FacebookStatus(models.Model):

    class Meta:
        verbose_name_plural = 'Facebook Statuses'
        ordering = ['publish_timestamp']

    STATUS = (
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    )
    status = models.CharField(max_length=25,
        choices=STATUS, default=STATUS[0][0])
    publish_timestamp = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User)
    message = models.TextField(max_length=255)
    link = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.message
from django.db import models


class TimeStampedModel(models.Model):
    """
    created , modified filed를 제공해주는 abstract base class model
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Log(TimeStampedModel):
    company_name = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
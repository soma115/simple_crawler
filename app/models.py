from django.db import models
from django.core.urlresolvers import reverse


class WebsiteCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('category_details_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Website(models.Model):
    url = models.URLField(blank=True, null=True, verbose_name='URL')
    title = models.CharField(max_length=400, blank=True, null=True, verbose_name='Title')
    meta_description = models.TextField(blank=True, null=True, verbose_name='Meta description')
    alexa_rank = models.IntegerField(blank=True, null=True, verbose_name='Alexa rank')
    category = models.ForeignKey(WebsiteCategory, on_delete=models.CASCADE, verbose_name='Category')
    date_added = models.DateTimeField(blank=True, null=True, verbose_name='Added')
    date_updated = models.DateTimeField(blank=True, null=True, verbose_name='Updated')

    def __str__(self):
        return self.url


class WebPage(models.Model):
    website = models.ForeignKey(Website)
    url = models.URLField(unique=True, max_length=1000)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.url



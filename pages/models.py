import markdown

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    content = models.TextField(
        help_text='Accepts Markdown, like Reddit comments but better.'
    )
    content_html = models.TextField(blank=True, default='')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.content_html = markdown.markdown(self.content)
        self.updated = timezone.now()
        return super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages_show_page', kwargs={'slug': self.slug})

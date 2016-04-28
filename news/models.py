import markdown

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class NewsPost(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, db_index=True)
    content = models.TextField(
        help_text='Accepts Markdown, like Reddit comments but better.'
    )
    content_html = models.TextField(blank=True, default='')
    created = models.DateTimeField(default=timezone.now, db_index=True)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.content_html = markdown.markdown(self.content)
        self.updated = timezone.now()
        return super(NewsPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_post_detail', kwargs={
            'year': self.created.year,
            'month': self.created.strftime("%m"),
            'day': self.created.strftime("%d"),
            'slug': self.slug,
        })

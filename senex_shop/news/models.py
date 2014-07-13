import datetime

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from managers import PublicManager

USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('news_category_detail', None, {'slug': self.slug})

    def save(self, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(**kwargs)


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(USER_MODULE_PATH, blank=True, null=True)
    body = models.TextField(_('body'), )
    tease = models.TextField(_('tease'), blank=True,
                             help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='posts')
    photo = models.ImageField(upload_to='photos/%Y/%b/%d', blank=True)
    # tags = TagField()
    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('news_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)

    def save(self, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        super(Post, self).save(**kwargs)

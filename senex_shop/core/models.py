from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from localflavor.us.models import USStateField, PhoneNumberField

from easy_thumbnails.fields import ThumbnailerImageField


class Address(models.Model):
    address_1 = models.CharField(
        _("address"),
        max_length=128,
        help_text=_("Address 1"),
    )
    address_2 = models.CharField(
        _("additional address"),
        max_length=128,
        blank=True,
        help_text=_("Address 2"),
    )
    city = models.CharField(
        _("city"),
        max_length=64,
        help_text=_("City"),
    )
    state = USStateField(
        _("state"),
        help_text=_("State"),
    )
    zip_code = models.CharField(
        _("zip code"),
        max_length=10,
        help_text=_("Zip Code (xxxxx or xxxxx-xxxx)"),
    )
    country = CountryField()

    class Meta:
        abstract = True


class Shop(Address):
    name = models.CharField(
        _(u"name"),
        max_length=30,
        help_text=_(u"The name of the shop"),
    )
    shop_owner = models.CharField(
        _(u"shop owner"),
        max_length=100,
        blank=True,
        help_text=_(u"The owner of the shop"),
    )
    from_email = models.EmailField(
        _(u"from e-mail address"),
        help_text=_(u"Email address to send e-mails with"),
    )
    description = models.TextField(
        _(u"description"),
        blank=True,
        help_text=_(u"A description about the shop"),
    )
    image = ThumbnailerImageField(
        _("image"),
        upload_to='product',
        blank=True,
        null=True,
        help_text=_("The product image used for display.")
    )
    phone = PhoneNumberField(
        _('phone'),
        help_text=_("The phone number of the company."),
    )
    meta_title = models.CharField(
        _(u"meta title"),
        blank=True,
        default="<name>",
        max_length=80,
        help_text=_(u"The meta title for the site"),
    )
    meta_keywords = models.TextField(
        _(u"meta keywords"),
        blank=True,
        help_text=_(u"The meta keywords for the site"),
    )
    meta_description = models.TextField(
        _(u"meta description"),
        blank=True,
        help_text=_(u"The meta description for the site"),
    )

    class Meta:
        permissions = (('manage_shop', "Manage shop"),)

    def __unicode__(self):
        return self.name

    def get_meta_title(self):
        return self.meta_title.replace("<name>", self.name)

    def get_meta_keywords(self):
        return self.meta_keywords.replace("<name>", self.name)

    def get_meta_description(self):
        return self.meta_description.replace("<name>", self.name)

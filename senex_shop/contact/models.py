"""
Stores customer, organization, and order information.
"""
import string
import zlib

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USStateField

USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# class Contact(models.Model):
#     """
#     A customer, supplier, or any individual that a store owner might interact with.
#     """
#     title = models.CharField(
#         _("title"),
#         max_length=30,
#         blank=True,
#         null=True,
#         help_text=_("The title of the contact."),
#     )
#     full_name = models.CharField(
#         _("first name"),
#         max_length=30,
#         help_text=_("The name of the contact."),
#     )
#     user = models.ForeignKey(
#         USER_MODULE_PATH,
#         blank=True,
#         null=True,
#         unique=True,
#         help_text=_("The user model associated with the contact if the contact registers."),
#     )
#     dob = models.DateField(
#         _("date of birth"),
#         blank=True,
#         null=True,
#         help_text=_("The date of birth of the contact."),
#     )
#     email = models.EmailField(
#         _("email"),
#         blank=True,
#         max_length=75,
#         help_text=_("The email address of the contact."),
#     )
#     stripe_id = models.CharField(
#         _("stripe customer id"),
#         max_length=100,
#         blank=True,
#         null=True,
#         help_text=_("The stripe customer is of the contact."),
#     )
#     notes = models.TextField(
#         _("notes"),
#         max_length=500,
#         blank=True,
#         help_text=_("Notes about the contact."),
#     )
#     created = models.DateTimeField(
#         _("created"),
#         auto_now_add=True,
#         help_text=_("The date and time that the contact was added."),
#     )
#
#     def _get_full_name(self):
#         """Return the person's full name"""
#         return u"{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)
#     full_name = property(_get_full_name)
#
#     def _shipping_address(self):
#         """Return the default shipping address or None"""
#         try:
#             return self.addressbook_set.get(is_default_shipping=True)
#         except AddressBook.DoesNotExist:
#             return None
#     shipping_address = property(_shipping_address)
#
#     def _billing_address(self):
#         """Return the default billing address or None."""
#         try:
#             return self.addressbook_set.get(is_default_billing=True)
#         except AddressBook.DoesNotExist:
#             return None
#     billing_address = property(_billing_address)
#
#     def _primary_phone(self):
#         """Return the default phone number or None."""
#         try:
#             return self.phonenumber_set.get(primary=True)
#         except PhoneNumber.DoesNotExist:
#             return None
#     primary_phone = property(_primary_phone)
#
#     def __unicode__(self):
#         return self.full_name
#
#     def save(self, **kwargs):
#         # Validate contact to user sync
#         if self.user:
#             dirty = False
#             user = self.user
#             if user.email != self.email:
#                 user.email = self.email
#                 dirty = True
#
#             if user.first_name != self.first_name:
#                 user.first_name = self.first_name
#                 dirty = True
#
#             if user.last_name != self.last_name:
#                 user.last_name = self.last_name
#                 dirty = True
#
#             if dirty:
#                 self.user = user
#                 self.user.save()
#
#         super(Contact, self).save(**kwargs)
#
#     def _get_address_book_entries(self):
#         """ Return all non primary shipping and billing addresses"""
#         return AddressBook.objects.filter(contact=self.pk).exclude(is_default_shipping=True).exclude(is_default_billing=True)
#
#     address_book_entries=property(_get_address_book_entries)
#
#     class Meta:
#         verbose_name = _("Contact")
#         verbose_name_plural = _("Contacts")
#
#
# PHONE_CHOICES = (
#     ('Work', _('Work')),
#     ('Home', _('Home')),
#     ('Fax', _('Fax')),
#     ('Mobile', _('Mobile')),
# )
#
#
# class PhoneNumber(models.Model):
#     """
#     Phone number associated with a contact.
#     """
#     contact = models.ForeignKey(Contact)
#     type = models.CharField(
#         _("description"),
#         choices=PHONE_CHOICES,
#         max_length=20,
#         blank=True,
#         help_text=_("The type of phone number."),
#     )
#     phone = models.CharField(
#         _("phone number"),
#         blank=True,
#         max_length=30,
#         help_text=_("The phone number.")
#     )
#     primary = models.BooleanField(
#         _("primary"),
#         default=False,
#         help_text=_("Is this the main number for the contact?"),
#     )
#
#     def __unicode__(self):
#         return u'%s - %s' % (self.type, self.phone)
#
#     def save(self, **kwargs):
#         """
#         If this number is the default, then make sure that it is the only
#         primary phone number. If there is no existing default, then make
#         this number the default.
#         """
#         existing_number = self.contact.primary_phone
#         if existing_number:
#             if self.primary:
#                 existing_number.primary = False
#                 super(PhoneNumber, existing_number).save()
#         else:
#             self.primary = True
#         super(PhoneNumber, self).save(**kwargs)
#
#     class Meta:
#         ordering = ['-primary']
#         verbose_name = _("Phone Number")
#         verbose_name_plural = _("Phone Numbers")
#

class AbstractAddress(models.Model):
    """
    Address information associated with a contact.
    """
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
        null=True,
    )
    street1 = models.CharField(
        _("street 1"),
        max_length=80,
        help_text=_("The street 1 field."),
    )
    street2 = models.CharField(
        _("street 2"),
        max_length=80,
        blank=True,
        help_text=_("APT/SUITE/OTHER"),
    )
    city = models.CharField(
        _("city"),
        max_length=50,
        help_text=_("The city field."),
    )
    state = USStateField(
        _("state"),
        max_length=50,
        blank=True,
        help_text=_("The state field."),
    )
    postal_code = models.CharField(
        _("zip code"),
        max_length=30,
        help_text=_("The postal code field."),
    )
    country = models.CharField(
        _("country"),
        default="United States",
        max_length=100,
        help_text=_("The country field."),
    )

    def active_address_fields(self):
        """
        Return the non-empty components of the address, but merging the
        title, first_name and last_name into a single line.
        """
        fields = [self.full_name, self.street1, self.street2,
                  self.city_state, self.postal_code, self.country]
        fields = map(string.strip, filter(bool, fields))
        return fields

    def clean(self):
        """Strip whitespace"""
        for field in ['full_name', 'street1', 'street2', 'city', 'state', 'postal_code', 'country', ]:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()

    def generate_hash(self):
        """
        Returns a hash of the address summary
        """
        return zlib.crc32(self.summary.strip().upper().encode('UTF8'))

    def populate_alternative_model(self, address_model):
        destination_field_names = [field.name for field in address_model._meta.fields]
        for field_name in [field.name for field in self._meta.fields]:
            if field_name in destination_field_names and field_name != 'id':
                setattr(address_model, field_name, getattr(self, field_name))


    @property
    def summary(self):
        return u", ".join(self.active_address_fields())

    @property
    def city_state(self):
        return u"{}, {}".format(self.city, self.state)

    def __unicode__(self):
        return u"{}".format(self.street1)


    class Meta:
        abstract = True
        verbose_name = _("address")
        verbose_name_plural = _("addresses")


class ShippingAddress(AbstractAddress):
    """
    A shipping address.
    """
    phone_number = models.CharField(
        _("phone number"),
        max_length=32,
        blank=True,
        null=True,
        help_text=_("In case we need to call you about your order."),
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("instructions"),
        help_text=("Tell us anything we should know when delivering your order."),
    )

    class Meta:
        verbose_name = _("shipping address")
        verbose_name_plural = _("shipping addresses")


class UserAddress(ShippingAddress):
    user = models.ForeignKey(
        USER_MODULE_PATH,
        related_name='addresses',
        verbose_name=_("user"),
    )
    is_default_shipping = models.BooleanField(
        _("default shipping address"),
        default=False,
        help_text=_("This is the default shipping address."),
    )
    is_default_billing = models.BooleanField(
        _("default billing address"),
        default=False,
        help_text=_("This is the default billing address."),
    )
    num_orders = models.PositiveIntegerField(
        _("number of orders"),
        default=0,
    )
    hash = models.CharField(
        _("address hash"),
        max_length=255,
        db_index=True,
        editable=False,
    )

    def _ensure_defaults_integrity(self):
        if self.is_default_shipping:
            self.__class__.__default_manager.filter(
                user=self.user,
                is_default_shipping=True
            ).update(
                is_default_shipping=False
            )
        if self.is_default_billing:
            self.__class__.__default_manager.filter(
                user=self.user,
                is_default_billing=True
            ).update(
                is_default_billing=False
            )

    def save(self, *args, **kwargs):
        """
        Save the hash of the address fields
        """
        self.hash = self.generate_hash()

        # Ensure default integrity
        self._ensure_defaults_integrity()
        super(UserAddress, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("user address")
        verbose_name_plural = _("user addresses")
        ordering = ['-num_orders']


class BillingAddress(AbstractAddress):
    class Meta:
        verbose_name = _("billing address")
        verbose_name_plural = _("billing addresses")

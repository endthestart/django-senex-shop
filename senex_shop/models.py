# from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import force_unicode, smart_str
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField

from . import active_product_types

dimension_units = (('cm', 'cm'), ('mm', 'mm'), ('in', 'in'))

weight_units = (('kg', 'kg'), ('lb', 'lb'))


def default_dimension_unit():
    return 'mm'


def default_weight_unit():
    return 'lb'


class Category(models.Model):
    """
    Basic hierarchical category model for storing products
    """
    name = models.CharField(
        _("name"),
        max_length=200,
    )
    slug = models.SlugField(
        _("slug"),
        help_text=_("Used for URLs, auto-generated from name if blank"),
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
    )
    path = models.CharField(
        _("path"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The path of the category for use in URLs"),
    )
    name_path = models.CharField(
        _("name path"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The path of the category for use in text"),
    )
    image = ThumbnailerImageField(
        _("image"),
        upload_to='category',
        blank=True,
        null=True,
        help_text=_("The category image used for display.")
    )
    meta = models.TextField(
        _("meta description"),
        blank=True,
        null=True,
        help_text=_("Meta description for this category."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Description of the category."),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override alphabetical order in the category display."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        blank=True,
        help_text=_("Whether or not the category is active."),
    )
    related_categories = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        verbose_name=_('related categories'),
        related_name='related_categories',
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return u"{0}".format(self.name)

    def get_ancestors(self):
        ancestors = []
        if self.parent:
            parent = self.parent
            while parent:
                ancestors.append(parent)
                parent = parent.parent
        ancestors.reverse()
        ancestors = ancestors + [self, ]
        return ancestors

    def join_path(self, joiner, field, ancestors):
        return joiner.join([force_unicode(getattr(i, field)) for i in ancestors])

    def _get_main_image(self):
        img = False
        return img

    main_image = property(_get_main_image)

    def save(self, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        ancestors = self.get_ancestors()
        self.path = self.join_path(u'/', 'slug', ancestors)
        self.name_path = self.join_path(u' > ', 'name', ancestors)

        super(Category, self).save(**kwargs)

        if self.child.all():
            children = list(self.child.all())
            for child in children:
                child.is_active = self.is_active
                child.save()

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'path': self.path})


# class CurrencyField(models.DecimalField):
#     __metaclass__ = models.SubfieldBase
#
#     def to_python(self, value):
#         try:
#             return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
#         except AttributeError:
#             return None

class Product(models.Model):
    """
    A class for items that can be ordered.
    """
    name = models.CharField(
        _("name"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The name of the product."),
    )
    slug = models.SlugField(
        _("slug"),
        blank=True,
        help_text=_("Used for URLs, auto-generated from name if blank."),
        max_length=255,
    )
    sku = models.CharField(
        _("sku"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Defaults to slug if left blank.")
    )
    created = models.DateTimeField(
        _("date created"),
        auto_now_add=True,
        help_text=_("The date and time the item was created."),
    )
    modified = models.DateTimeField(
        _("date modified"),
        auto_now=True,
        help_text=_("The date and time the item was modified."),
    )
    category = models.ForeignKey(
        Category,
        related_name=_("category"),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override default alphabetical ordering"),
    )
    price = models.DecimalField(
        _("price"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The cost of the item."),
    )
    stock = models.IntegerField(
        _("stock"),
        default='0',
    )
    short_description = models.TextField(
        _("short description of the product."),
        max_length=200,
        default='',
        blank=True,
        help_text=_("This should be a 1 or 2 line description of the product."),
    )
    description = models.TextField(
        _("description"),
        null=True,
        blank=True,
        help_text=_("This should be a more lengthy description of the product."),
    )
    meta = models.TextField(
        _("meta description"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("The meta description of the product."),
    )
    active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Denotes if the product is available or not."),
    )

    # objects = ProductManager()

    def _get_main_category(self):
        """Return the first category for the product"""
        if self.category.count() > 0:
            return self.category.all()[0]
        else:
            return None

    main_category = property(_get_main_category)

    def _get_main_image(self):
        img = False
        if self.productimage_set.count() > 0:
            img = self.productimage_set.order_by('sort')[0]

        if not img:
            try:
                img = ProductImage.objects.filter(product__isnull=True).order_by('sort')[0]
                img = None
            except IndexError:
                #TODO: Remove this code when updating images
                import sys
                print >> sys.stderr, 'Warning: default product image not found'
        return img

    main_image = property(_get_main_image)

    def _get_full_price(self):
        return self.price

    unit_price = property(_get_full_price)

    def _in_stock(self):
        return self.stock > 0

    is_in_stock = property(_in_stock)

    def _available(self):
        return True

    is_available = property(_available)

    def _get_category(self):
        """
        Return the primary category associated with this product
        """
        try:
            return self.category.all()[0]
        except IndexError:
            return None

    get_category = property(_get_category)

    def get_subtypes(self):
        if hasattr(self, "_sub_types"):
            return self._sub_types
        types = []
        try:
            for module, subtype in active_product_types():
                try:
                    subclass = getattr(self, subtype.lower())
                    if subclass is not None:
                        gettype = getattr(subclass, '_get_subtype')
                        subtype = gettype()
                        if not subtype in types:
                            types.append(subtype)
                except models.ObjectDoesNotExist:
                    pass
        except:
            pass

        self._sub_types = tuple(types)
        return self._sub_types

    get_subtypes.short_description = _("product subtypes")

    def add_template_context(self, context, *args, **kwargs):
        subtypes = self.get_subtypes()
        for subtype_name in subtypes:
            subtype = getattr(self, subtype_name.lower())
            if subtype == self:
                continue
            if hasattr(subtype, 'add_template_context'):
                context = subtype.add_template_context(context, *args, **kwargs)

        return context

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', (), {'slug': self.slug, 'path': self.category.path})

    class Meta:
        ordering = ('ordering', 'name')
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def save(self, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super(Product, self).save(**kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, )
    image = ThumbnailerImageField(
        _("image"),
        upload_to='product',
        blank=True,
        null=True,
        help_text=_("The product image used for display.")
    )
    sort = models.IntegerField(_("Sort Order"), default=0)

    class Meta:
        ordering = ['sort']
        unique_together = (('product', 'sort'),)
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class OptionGroupManager(models.Manager):
    def get_sortmap(self):
        """Returns a dictionary mapping ids to sort order"""

        work = {}
        for uid, order in self.values_list('id', 'ordering'):
            work[uid] = order

        return work


class OptionGroup(models.Model):
    name = models.CharField(
        _("name"),
        max_length=50,
        help_text=_("The name of the option group."),
    )
    description = models.TextField(
        _("description"),
        null=True,
        blank=True,
        help_text=_("This should be a more lengthy description of the option group."),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override alphabetical order in the category display."),
    )

    objects = OptionGroupManager()

    class Meta:
        ordering = ('ordering',)
        verbose_name = _("option group")
        verbose_name_plural = _("option groups")

    def __unicode__(self):
        if self.description:
            return u'{0} - {1}'.format(self.name, self.description)
        else:
            return self.name


class OptionManager(models.Manager):
    def from_unique_id(self, unique_id):
        group_id, option_value = split_option_unique_id(unique_id)
        group = OptionGroup.objects.get(id=group_id)
        return Option.objects.get(option_group=group_id, value=option_value)


class Option(models.Model):
    """
    The actual options in an option group.
    """
    option_group = models.ForeignKey(OptionGroup)
    name = models.CharField(
        _("name"),
        max_length=50,
        help_text=_("The displayed value of the option."),
    )
    value = models.CharField(
        _("value"),
        max_length=50,
        help_text=_("The stored value of the option.")
    )
    price_change = models.DecimalField(
        _("price change"),
        max_digits=8,
        decimal_places=2,
        default=0.00,
        help_text=_("The change in cost for a product."),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override alphabetical order in the category display."),
    )

    class Meta:
        ordering = ('option_group', 'ordering')
        unique_together = (('option_group', 'value'),)
        verbose_name = _("option")
        verbose_name_plural = _("options")

    def _get_unique_id(self):
        return make_option_unique_id(self.option_group_id, self.value)

    unique_id = property(_get_unique_id)

    def __unicode__(self):
        return u'{0}: {1}'.format(self.option_group.name, self.name)


# Support the user's setting of custom expressions in the settings.py file
#try:
#    user_validations = settings.SATCHMO_SETTINGS.get('ATTRIBUTE_VALIDATIONS')
#except:
#    user_validations = None

VALIDATIONS = [
    ('product.utils.validation_simple', _('One or more characters')),
    ('product.utils.validation_integer', _('Integer number')),
    ('product.utils.validation_yesno', _('Yes or No')),
    ('product.utils.validation_decimal', _('Decimal number')),
]
#if user_validations:
#    VALIDATIONS.extend(user_validations)


class AttributeOption(models.Model):
    """
    Allows arbitrary name/value pairs to be attached to a product.
    By defining the list, the user will be presented with a predefined
    list of attributes instead of a free form field.
    The validation field should contain a regular expression that can be
    used to validate the structure of the input.
    Possible usage for a book:
    ISBN, Pages, Author, etc
    """
    description = models.CharField(
        _("description"),
        max_length=100,
    )
    name = models.SlugField(
        _("name"),
        max_length=100,
    )
    validation = models.CharField(
        _("validation"),
        choices=VALIDATIONS,
        max_length=100,
    )
    sort_order = models.IntegerField(
        _("sort order"),
        default=1,
    )
    error_message = models.CharField(
        _("error message"),
        default=_("invalid entry"),
        max_length=100,
    )

    class Meta:
        ordering = ('sort_order',)

    def __unicode__(self):
        return self.description


class ProductAttribute(models.Model):
    """
    Allows arbitrary name/value pairs (as strings) to be attached to a product.
    This is a simple way to add extra text or numeric info to a product.
    If you want more structure than this, create your own subtype to add
    whatever you want to your Products.
    """
    product = models.ForeignKey(Product)
    option = models.ForeignKey(AttributeOption)
    value = models.CharField(
        _("value"),
        max_length=255
    )

    def _name(self):
        return self.option.name

    name = property(_name)

    def _description(self):
        return self.option.description

    description = property(_description)

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        ordering = ('option__sort_order',)


    def __unicode__(self):
        return self.option.name


def make_option_unique_id(groupid, value):
    return '%s-%s' % (smart_str(groupid), smart_str(value),)


def split_option_unique_id(uid):
    """
    reverse of make_option_unique_id
    """
    parts = uid.split('-')
    return (parts[0], '-'.join(parts[1:]))

#from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#from django.template.loader import select_template

from .models import Category, Product, OptionGroup


def find_product_template(product, product_types=None):
    if product_types is None:
        product_types = product.get_subtypes()

    templates = ["senex_shop/detail_%s.html" % x.lower() for x in product_types]
    templates.append('senex_shop/product.html')
    return templates[0]


def store_home(request, template_name="senex_shop/category.html"):
    categories = Category.objects.filter(parent=None)
    context = {
        'child_categories': categories
    }
    return render_to_response(template_name, context, RequestContext(request))


def category(request, path=None, template_name="senex_shop/category.html"):
    category = get_object_or_404(Category, path=path)
    child_categories = Category.objects.filter(parent=category)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'child_categories': child_categories,
        'products': products
    }

    return render_to_response(template_name, context, RequestContext(request))


def product_detail(request, path=None, slug=None, selected_options=(), template_name="senex_shop/product.html"):
    #errors = [m for m in get_messages(request) if m.level == constants.ERROR]
    product = get_object_or_404(Product, active=True, slug=slug)

    subtype_names = product.get_subtypes()

    product_id = product.id
    current_product = product

    context = {
        'product': product,
        'current_product': current_product,
    }

    context = product.add_template_context(
        context=context,
        request=request,
        selected_options=selected_options
    )

    template_name = find_product_template(product, product_types=subtype_names)

    return render_to_response(template_name, context, RequestContext(request))


def email_check(request):

    context = {
        'billing_name': "Billing Name",
    }

    return render_to_response('senex_shop/email/order_confirmation.html', context, RequestContext(request))

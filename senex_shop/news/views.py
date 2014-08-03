from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView

from models import Post, Category


def post_detail(request, slug, year, month, day, template_name='senex_shop/news/post_detail.html'):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.all()
    context = {
        'post': post,
        'categories': categories,
    }
    return render_to_response(template_name, context, RequestContext(request))


class PostListView(ListView):
    model = Post
    template_name = 'senex_shop/news/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

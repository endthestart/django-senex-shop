from django.conf.urls import patterns, url
from views import PostListView, post_detail


urlpatterns = patterns('',
                       url(
                           r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
                           view=post_detail,
                           name='news_detail'
                       ),
                       # url(
                       #     r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
                       #     view='post_archive_day',
                       #     name='news_archive_day'
                       # ),
                       # url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', view='post_archive_month',
                       #     name='news_archive_month'),
                       # url(r'^(?P<year>\d{4})/$', view='post_archive_year', name='news_archive_year'),
                       # url(r'^page/(?P<page>\d+)/$', view='post_list', name='news_index_paginated'),
                       url(r'^$', PostListView.as_view(), name='news_index'),
)
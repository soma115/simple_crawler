from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from app.views import website_all_view, website_details_view, website_new_view, \
    website_edit_view, website_delete_view
from app.views import category_all_view, category_details_view, category_new_view, \
    category_edit_view, category_delete_view
from app.views import read_links


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="app/home.html")),

    url(r'^website/$', view=website_all_view, name='website_all_url'),
    url(r'^website/new/$', view=website_new_view, name='website_new_url'),
    url(r'^website/(?P<pk>[0-9]+)/details/$', view=website_details_view, name='website_details_url'),
    url(r'^website/(?P<pk>[0-9]+)/edit/$', view=website_edit_view, name='website_edit_url'),
    url(r'^website/(?P<pk>[0-9]+)/delete/$', website_delete_view.as_view(), name="website_delete_url"),

    url(r'^website/(?P<pk>[0-9]+)/scan/$', view=read_links, name="website_scan_url"),

    url(r'^category/$', view=category_all_view, name='category_all_url'),
    url(r'^category/new/$', view=category_new_view, name='category_new_url'),
    url(r'^category/(?P<pk>[0-9]+)/details/$', view=category_details_view, name='category_details_url'),
    url(r'^category/(?P<pk>[0-9]+)/edit/$', view=category_edit_view, name='category_edit_url'),
    url(r'^category/(?P<pk>[0-9]+)/delete/$', category_delete_view.as_view(), name="category_delete_url"),
]


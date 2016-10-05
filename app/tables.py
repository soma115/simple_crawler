import django_tables2 as dt2
from .models import Website, WebsiteCategory
from django_tables2.utils import A


class WebsiteTable(dt2.Table):
    title = dt2.LinkColumn(viewname='website_details_url', text=lambda record: record.title, args=[A('pk')])

    class Meta:
        model = Website
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        exclude = ('id', )      # ('id') without comma will not work!


class CategoryTable(dt2.Table):
    title = dt2.LinkColumn(viewname='category_details_url', text=lambda record: record.name, args=[A('pk')])

    class Meta:
        model = WebsiteCategory
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        exclude = ('id', )      # ('id') without comma will not work!

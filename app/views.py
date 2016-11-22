from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.edit import DeleteView # this is the generic view
from .models import WebsiteCategory, Website, WebPage
from .tables import WebsiteTable, CategoryTable
from .forms import WebsiteForm, WebsiteCategoryForm
from django_tables2 import RequestConfig
from celery.task import task
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.db import IntegrityError


#TODO: Przerobic funkcje na obiekty
#TODO: remove duplicates
#TODO: webPAGE_details_view + skanowanie


def website_all_view(request):

    a = Website.objects.all()
    query = request.GET.get('q')

    if query:
        a = a.filter(
            Q(category__name__icontains=query)
        ).distinct()

    table = WebsiteTable(a)
    RequestConfig(request).configure(table)

    return render(request, 'app/website_list.html', {'table': table})


def website_details_view(request, pk):
    details = get_object_or_404(Website, pk=pk)
    return render(request, 'app/website_details.html', {'details': details})


def website_new_view(request):
    if request.method == "POST":
        form = WebsiteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.url = form.cleaned_data['url']
            post.date_added = timezone.now()
            post.save()
            return redirect('website_details_url', pk=post.pk)
    else:
        form = WebsiteForm()
    return render(request, 'app/website_edit.html', {'form': form})


def website_edit_view(request, pk):
    post = get_object_or_404(Website, pk=pk)

    if request.method == "POST":
        form = WebsiteForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_updated = timezone.now()
            post.url = form.data.values()[0]
            post.save()
            return redirect('website_details_url', pk=post.pk)
    else:
        form = WebsiteForm(instance=post)
    return render(request, 'app/website_edit.html', {'form': form})


class website_delete_view(DeleteView):
    model = Website
    success_url = reverse_lazy('website_all_url') # This is where this view will redirect the user
    template_name = 'app/delete_note.html'


##############################################


def category_all_view(request):

    a = WebsiteCategory.objects.all()
    table = CategoryTable(a)
    RequestConfig(request).configure(table)

    return render(request, 'app/category_list.html', {'table': table})


def category_details_view(request, pk):
    details = get_object_or_404(WebsiteCategory, pk=pk)
    return render(request, 'app/category_details.html', {'details': details})


def category_new_view(request):
    if request.method == "POST":
        form = WebsiteCategoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_added = timezone.now()
            post.save()
            return redirect('category_details_url', pk=post.pk)
    else:
        form = WebsiteCategoryForm()
    return render(request, 'app/category_edit.html', {'form': form})


def category_edit_view(request, pk):
    post = get_object_or_404(WebsiteCategory, pk=pk)

    if request.method == "POST":
        form = WebsiteCategoryForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_updated = timezone.now()
            post.save()
            return redirect('category_details_url', pk=post.pk)
    else:
        form = WebsiteCategoryForm(instance=post)
    return render(request, 'app/category_edit.html', {'form': form})


class category_delete_view(DeleteView):
    model = WebsiteCategory
    success_url = reverse_lazy('category_all_url') # This is where this view will redirect the user
    template_name = 'app/delete_note.html'

##############################################


@task()
def read_links(request, pk):
    post = get_object_or_404(Website, pk=pk)
    url = post.url
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    links = soup.find_all('a')
    tab = []

    for i in links:
        link = str(i.get('href', None))
        if link.startswith('#') or link == "/" or link is None or str(link).__contains__('?') or \
                link.startswith('mailto:'):
            continue
        if link.startswith('http://www.') or str(link).startswith('https://www.'):
            link=(str(link).replace('://www.', '://'))    # some link got 'www' in front
        if link.startswith('//'):
            link=('http:'+link)
        if link.startswith("/"):
            link=(url + str(link))
        if link:
            tab.append(link)

    list_of_links = list(set(tab))  # make unique
    for i in list_of_links:
        try:
            a = WebPage(url=i, pk=None, website=Website(id=pk))
            a.save()
            continue
        except IntegrityError:
            pass

    return render(request, 'app/website_scan.html')



'''
url = 'http://stowarzyszenie.demokracjabezposrednia.pl'

app = Celery('tasks', broker='amqp://localhost//')
app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(settings.INSTALLED_APPS)

    url cleanning:
            # #=anchor, /=root, None=no links, ?=parameter for local link
            # <a href="#main-content-area">     zignorowac
            # <a href="/"                       zignorowac
            # <a href="/jak_pomoc"              dopisac na poczatku url pochodzenia

    # @app.task
    # def add(x, y):
    #     return x * y
    #
    # add.delay(9,9)


'''






from django.contrib import admin
from .models import Website, WebsiteCategory, WebPage

admin.site.register(Website)
admin.site.register(WebsiteCategory)
admin.site.register(WebPage)

from django.contrib import admin
from .models import Website, WebsiteCategory, WebPage

# Register your models here.
admin.site.register(Website)
admin.site.register(WebsiteCategory)
admin.site.register(WebPage)


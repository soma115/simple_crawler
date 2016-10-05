from django import forms
from .models import Website, WebsiteCategory


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('title', 'url', 'category',)


class WebsiteCategoryForm(forms.ModelForm):
    class Meta:
        model = WebsiteCategory
        fields = ('name', 'description',)

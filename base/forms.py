from django import forms
from django.forms import ModelForm
from base.models import Franchise

class FranciseForm(ModelForm):
    twitter_handle = forms.CharField(max_length=200, required=False)
    twitter_url = forms.URLField(required=False)

    reddit_handle = forms.CharField(max_length=200, required=False)
    reddit_url = forms.URLField(required=False)

    website_handle = forms.CharField(max_length=200, required=False)
    website_url = forms.URLField(required=False)

    instagram_handle = forms.CharField(max_length=200, required=False)
    instagram_url = forms.URLField(required=False)

    youtube_handle = forms.CharField(max_length=200, required=False)
    youtube_url = forms.URLField(required=False)

    class Meta:
        model = Franchise
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        socials_data = {}

        platforms = ['twitter', 'reddit', 'instagram', 'website', 'youtube']

        for platform in platforms:
            handle = cleaned_data.get(f'{platform}_handle')
            url = cleaned_data.get(f'{platform}_url')

            if handle != "" and url != "":
                socials_data[platform] = {
                    'handle': handle,
                    'url': url
                }

        self.instance.socials = socials_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.socials:
            socials = self.instance.socials
            for platform, data in socials.items():
                if f'{platform}_handle' in self.fields:
                    self.initial[f'{platform}_handle'] = data.get('handle')
                if f'{platform}_url' in self.fields:
                    self.initial[f'{platform}_url'] = data.get('url')
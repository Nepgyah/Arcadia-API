from django import forms
from miru.models.anime import AniListData

class AniListForm(forms.ModelForm):
    class Meta:
        model = AniListData
        fields = ['anilist_id']

    def clean_anilist_id(self):
        val = self.cleaned_data.get('anilist_id')

        if not val:
            raise forms.ValidationError("You must provide an anilist id to import")
        return val
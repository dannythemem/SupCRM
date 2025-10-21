from django import forms

from string import ascii_letters, digits
from .models import Posts, Tags

ALLOWED_CHARS = ascii_letters + digits + 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя-'

class AddPostForm(forms.ModelForm):
    tags_input = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите теги через пробел'}),
        required=False,
        label='Теги',
    )
    class Meta:
        model = Posts
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        fields = ['title', 'content', 'tags_input']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags_raw = self.cleaned_data['tags_input']
            tag_names = [name.strip() for name in tags_raw.split() if name.strip()]
            for tag_name in tag_names:
                clean_name = ''.join([i for i in tag_name if i in ALLOWED_CHARS])
                if not clean_name:
                    continue
                tag_obj, created = Tags.objects.get_or_create(title=clean_name)
                if created or not tag_obj.slug: tag_obj.save()
                instance.tags.add(tag_obj)
        return instance
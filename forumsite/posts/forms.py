from django import forms
from .models import Posts

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        fields = ['title', 'content']
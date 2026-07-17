from django import forms
from .models import Comment 

class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Your email'})
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Recipient email'})
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Optional comments'})
    )
    
class CommentForm(forms.ModelForm): 
    class Meta: # To create a form from a model
        model = Comment
        fields = ['name', 'email', 'body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Your name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your email'})
        self.fields['body'].widget.attrs.update({'placeholder': 'Your comment'})
        
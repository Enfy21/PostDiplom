from django import forms
from .models import PostModel, Comment
from django.forms import ModelForm, TextInput, DateTimeInput, EmailInput, \
    CheckboxInput, Select, NumberInput, DateInput, Textarea, PasswordInput



class PostModelForm(forms.ModelForm):
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = PostModel
        fields = ('title', 'content')
        labels = {
            'title': 'Тема поста',
        }
        widgets = {
            'title': TextInput(attrs={
                'class': 'input p-2 w-full max-w-lg input-bordered',
            }),
            'content': Textarea(attrs={
                'class': 'input p-2 w-full max-w-lg input-bordered',
            }),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'content')
        labels = {
            'title': 'Тема поста',
            'content': 'Контент',
        }
        widgets = {
            'title': TextInput(attrs={
                'class': 'input p-2 w-full max-w-lg input-bordered',
            }),
            'content': Textarea(attrs={
                'class': 'input p-2 w-full max-w-lg input-bordered',
            }),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Напишите свой комментарий', 'class': 'input p-2 w-full max-w-lg input-bordered',}))

    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Контент',
        }

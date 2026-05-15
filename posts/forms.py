from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '제목을 입력하세요',
                'class': 'w-full',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': '내용을 입력하세요',
                'rows': 8,
                'class': 'w-full',
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '이미지 (선택)',
        }


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': '댓글을 입력하세요',
                'rows': 2,
                'class': 'w-full resize-none',
            }),
        }
        labels = {
            'content': '',
        }

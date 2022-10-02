
from django import forms

from blog.models import BlogPost, Comment

class CreateBlogPostForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

class UpdateBlogPostForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']
    
    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']
        
        if commit:
            blog_post.save()
        return blog_post

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3', 'cols':'66',
                   'placeholder': 'Comment here...'}
        ))
    
    class Meta:
        model = Comment
        fields = ['comment']

class EditCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3', 'max-cols':'75',
                   'placeholder': 'Comment here...'}
        ))
    
    class Meta:
        model = Comment
        fields = ['comment']

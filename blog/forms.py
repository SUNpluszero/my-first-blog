from django import forms

from .models import Post, Comment, Document


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class UserForm(forms.Form):

	username = forms.CharField(max_length=150)
	password = forms.CharField(max_length=100)
	email = forms.EmailField()
	password_check = forms.CharField(max_length=100)


	def is_valid(self):
		valid = super(UserForm, self).is_valid()
		return valid and self.cleaned_data['password'] == self.cleaned_data['password_check']

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('description', 'document',);
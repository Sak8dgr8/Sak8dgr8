from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile
from .models import Project
from .models import Comment, UpdateComment
from. models import Donation
from .models import Update
from django.forms import ImageField, FileInput


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)


		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

		
        
class ChannelCustomizationForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ('profile_pic', 'bio', 'cropped_image_data',)
		widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'custom-profile-pic-input', 'accept': 'image/*'}),
	   				'bio': forms.Textarea(attrs={'class': 'custom-bio-field'}),
	     
        }

	def __init__(self, *args, **kwargs):
		super(ChannelCustomizationForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget.attrs['class'] = 'form-control'
		
		


class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ('state','city','project_title', 'funding_goal', 'target_date','project_description', 'project_video', 'project_thumbnail')


	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		self.fields['city'].widget.attrs['class']='city-inpt'
		self.fields['target_date'].widget.attrs['class']='days-inpt'
		self.fields['state'].widget.attrs['class']='state-inpt'
		self.fields['project_title'].widget.attrs['class'] = 'form-inpt'
		self.fields['funding_goal'].widget.attrs['class'] = 'form-inpt'
		self.fields['project_description'].widget.attrs['class'] = 'form-inpt'

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['body']
		labels = {'body': ''}
		widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Share your thoughts...'})
        }
	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget.attrs['class']='comment-input'

class UpdateCommentForm(forms.ModelForm):

	class Meta:
		model = UpdateComment
		fields = ['body']
		labels = {'body':''}
		widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Share your thoughts...'})
        }
	def __init__(self, *args, **kwargs):
		super(UpdateCommentForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget.attrs['class']='comment-input'

		
class DonationForm(forms.ModelForm):


	class Meta:
		model = Donation
		fields = ['donation_amount', 'platform_donation', 'first_name', 'last_name', 'donor_email']
	
	def __init__(self, *args, **kwargs):
		super(DonationForm, self).__init__(*args, **kwargs)
		self.fields['donation_amount'].widget.attrs['class'] = 'donation-box'
		self.fields['donation_amount'].widget.attrs['placeholder'] = '00.00'
		self.fields['platform_donation'].widget.attrs['class'] = 'platform-box'
		self.fields['platform_donation'].widget.attrs['placeholder'] = '00.00'
		self.fields['first_name'].widget.attrs['class'] = 'name-box'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
		self.fields['last_name'].widget.attrs['class'] = 'name-box'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
		self.fields['donor_email'].widget.attrs['class'] = 'email-box'
		self.fields['donor_email'].widget.attrs['placeholder'] = 'Email'


class UpdateForm(forms.ModelForm):

	class Meta:
		model = Update
		fields = ['update_title', 'update_description', 'update_video', 'update_thumbnail']
		labels = {
            'update_video': 'Video (required)',
        }
		widgets = {
            'update_title': forms.TextInput(attrs={'class': 'update-title-input'}),
            'update_description': forms.Textarea(attrs={'class': 'update-description-input'}),
            'update_video': forms.FileInput(attrs={'accept': 'video/*'}),
            'update_thumbnail': forms.ClearableFileInput(attrs={'class': 'upload-area'}),
        }


	def __init__(self, *args, **kwargs):
		super(UpdateForm, self).__init__(*args, **kwargs)
		self.fields['update_title'].widget.attrs['class'] = 'update-title-input'
		self.fields['update_description'].widget.attrs['class'] = 'update-description-input'
		

from paypal.standard.forms import PayPalPaymentsForm

class PayPalPaymentsForm(PayPalPaymentsForm):
    def __init__(self, custom_image_url=None, *args, **kwargs):
        self.custom_image_url = custom_image_url
        super(PayPalPaymentsForm, self).__init__(*args, **kwargs)

    def get_image(self):
        if self.custom_image_url:
            return self.custom_image_url
        else:
            # Replace this with the default image URL
            return "https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif"

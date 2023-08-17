from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Again Password'

        self.fields['email'].help_text = "We'll never share your email with anyone else."
        self.fields['password2'].help_text = "Type the password again just for confirmation"


class AddEditRecordForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3, max_length=50, label="First Name")
    last_name = forms.CharField(min_length=3, max_length=70, label="Last Name")
    email = forms.EmailField(min_length=5, max_length=100)
    phone_number = forms.CharField(min_length=5, max_length=20)

    class Meta:
        model = Record
        fields = '__all__'

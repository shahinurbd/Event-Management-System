from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
from django.core.validators import RegexValidator
import re
from events.forms import StyleFormMixin

class CustomRegistrationForm(StyleFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password','confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
        regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if len(password) < 8:
            errors.append('password must be atleast 8 charecters long')
        if not re.match(regex, password):
            raise forms.ValidationError("Password must be at least 8 characters long, contain one uppercase letter, one number, and one special character.")


        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    def clean(self):    #non field error
        clean_data = super().clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password did not match')
        
        return clean_data
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email
    


class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)


class AssignRoleForm(StyleFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )


class CreateGroupForm(StyleFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name','permissions']


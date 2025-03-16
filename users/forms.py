from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
from django.core.validators import RegexValidator
import re
from events.forms import StyleFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

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


class CustomPasswordChangeForm(StyleFormMixin,PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyleFormMixin,PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyleFormMixin,SetPasswordForm):
    pass

class EditProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_image']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        errors = []
        regex = r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$'
        if len(phone_number) < 11:
            errors.append('phone number must be 11 digits')
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Invalid phone number. Use +8801XXXXXXXXX or 01XXXXXXXXX.")


        if errors:
            raise forms.ValidationError(errors)
        
        return phone_number



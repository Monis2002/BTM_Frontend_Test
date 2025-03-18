from django.contrib.auth.models import  User
from django.contrib.auth.forms import  UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile,Product,Business_type,Enquiry,BestPriceRequest


class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model=User
		fields=['new_password1','new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)


		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        }),
        required=True,
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }),
        required=True,
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }),
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'User Name',
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.</small>'
            '</span>'
        )

        # Customize password1 field
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password must include at least one uppercase letter, one lowercase letter, one digit, and one special character.</li>'
            '<li>Your password can\'t be a commonly used password or entirely numeric.</li>'
            '</ul>'
        )

        # Customize password2 field
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Enter the same password as before, for verification.</small>'
            '</span>'
        )

    def clean_password1(self):
        """
        Custom validation for the password1 field to enforce additional conditions.
        """
        password = self.cleaned_data.get('password1')

        # Apply custom password validation
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        

        return password



from django import forms
from .models import Profile, Business_type, City

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), 
        required=False
    )
    address1 = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}), 
        required=False
    )
    address2 = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), 
        required=False
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'City'}),
        required=False,
        label='',
    )
    state = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), 
        required=False
    )
    zipcode = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}), 
        required=False
    )
    country = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), 
        required=False
    )
    
    GST_number = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number'}), 
        required=False
    )
    work_days = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Days Eg: Mon-Fri'}), 
        required=False
    )
    employee_count = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Count'}), 
        required=False
    )
    company_details = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Details'}), 
        required=False
    )
    establishment = forms.DateField(
        label='', 
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Establishment: YYYY-MM-DD'}), 
        required=False
    )
    business_type = forms.ModelMultipleChoiceField(
        queryset=Business_type.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            'phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', 
            'GST_number', 'work_days', 'employee_count', 
            'company_details', 'establishment', 'business_type'
        )



class UpdateUserForm(UserChangeForm):
	# Hide Password
	password=None

	# Fetch all data
	email = forms.EmailField(label="",
							 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),required=False)
	first_name = forms.CharField(label="", max_length=100,
								 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),required=False)
	last_name = forms.CharField(label="", max_length=100,
								widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields[
			'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'



class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your contact number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here',
                'rows': 4
            }),
        }


from django import forms

class BestPriceForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    phone = forms.CharField(max_length=15, label="Your Phone Number")
    message = forms.CharField(widget=forms.Textarea, label="Message", required=False)


from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class NewPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

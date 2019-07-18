from django import forms
from login import validators
from .models import Accounts

class SignUpForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    contact_person = forms.CharField(label='Contact Person', max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    email_id = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password',validators=[validators.validate_password_strength], widget=forms.PasswordInput(attrs={"class":"form-control"}), max_length=50,
                               help_text='Password should contain at least one special character, one alphanumeric, one upper case and one lower case.')
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control"}), max_length=30)
    phone_number = forms.CharField(label='Phone Number',validators=[validators.phone_regex], max_length=30, help_text='Please include country code', widget=forms.TextInput(attrs={"class":"form-control"}))
    country = forms.CharField(label='Country', max_length=30, widget=forms.TextInput(attrs={"class":"form-control"}))

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        company_name = cleaned_data['company_name']
        email_id = cleaned_data['email_id']

        if Accounts.objects.filter(CompanyName=company_name).exists():
            return self.add_error("company_name","This CompanyName already exist")
        if Accounts.objects.filter(Email=email_id).exists():
            return self.add_error("email_id","This Email already exist")
        if confirm_password != password:
            return self.add_error("confirm_password","Password and Confirm Password does not match")


class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))


class LoginForm(forms.Form):
    email_id = forms.EmailField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password',  widget=forms.PasswordInput, max_length=50, required=True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email_id = cleaned_data.get("email_id")

        # if not Users.objects.filter(EmailId=email_id).exists():
        #      return self.add_error("email_id", "This Email does not exist")


class ForgotForm(forms.Form):
    email_id = forms.EmailField(label='Email', max_length=254, required=True)

    def clean(self):
        cleaned_data = super(ForgotForm, self).clean()
        email_id = cleaned_data.get("email_id")


class ResetForm(forms.Form):
    password = forms.CharField(label='Password', validators=[validators.validate_password_strength],widget=forms.PasswordInput, max_length=30)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=30)

    def clean(self):
        cleaned_data = super(ResetForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password != password:
            return self.add_error("confirm_password","Password and Confirm Password does not match")

COUNTRY_CHOICES= [
    ('USA', 'USA'),
    ]

class EditAccountForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_person = forms.CharField(label='Contact Person', max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email_id = forms.EmailField(label='Email', max_length=254, widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}))
    password = forms.CharField(label='Password', required=False, validators=[validators.validate_password_strength], widget=forms.PasswordInput(attrs={"class": "form-control", "id": "txtNewPassword"}), max_length=30,
                               help_text='Password should contain at least one special character, one alphanumeric, one upper case and one lower case.')
    confirm_password = forms.CharField(label='Confirm Password', required=False, widget=forms.PasswordInput(attrs={"class": "form-control", "id": "txtConfirmPassword"}), max_length=30)
    phone_number = forms.CharField(label='Phone Number', validators=[validators.phone_regex], max_length=30, help_text='Please include country code',widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(label='Country', max_length=30, widget=forms.Select(choices=COUNTRY_CHOICES, attrs={"class": "form-control"}))
    state = forms.CharField(label='State', max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label='Address', max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    zip_code = forms.CharField(label='Zip Code', max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


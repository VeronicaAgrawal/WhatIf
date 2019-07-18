from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

# Create your models here.
class Accounts(models.Model):
    CompanyName = models.CharField(max_length=30, unique=True, blank=False)
    ContactPerson = models.CharField(max_length=30, blank=False)
    Email = models.EmailField(max_length=100, unique=True, blank=False)
    Address = models.TextField(max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    PhoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    State = models.CharField(max_length=30, blank=True)
    Country = models.CharField(max_length=30, blank=False)
    Zip = models.CharField(max_length=30, blank=True)
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField()
    # Image = models.

    def get_user_details(email_id):
        dt = Accounts.objects.get(Email=email_id)
        return dt;

class Users(models.Model):
    EmailId = models.EmailField(max_length=100, unique=True, blank=False)
    PasswordEncrypted = models.CharField(max_length=50, blank=False)
    IsActive = models.BooleanField(default=True)
    IsStaff = models.BooleanField(default=False)  # a admin user; non super-user
    IsAdmin = models.BooleanField(default=False)  # a superuser
    CreatedOn = models.DateTimeField(auto_now_add=True)
    LastLogin = models.DateTimeField()
    AccountId = models.IntegerField()

    USERNAME_FIELD = 'EmailId'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        return make_password(raw_password)

    def check_pwd(self,user, password):
        return check_password(password ,user.PasswordEncrypted )

    def check_email(self, email_id):
        return Users.objects.get(EmailId=email_id)

    def get_userid(email_id):
        return Users.objects.get(EmailId=email_id).id
        #return user.id

@property
def is_staff(self):
    "Is the user a member of staff?"
    return self.IsStaff

@property
def is_admin(self):
    "Is the user a admin member?"
    return self.IsAdmin

@property
def is_active(self):
    "Is the user active?"
    return self.IsActive

@property
def is_authenticated(self):
    return True
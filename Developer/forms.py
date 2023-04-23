from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,DB_Fees
from django import forms
from django.contrib.auth.forms  import AuthenticationForm

class Custom_Institute_Creation_Form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'institute_name','institute_address','institute_code','institute_logo','is_institute','password1','password2')
 
class login_form(AuthenticationForm):
    username=forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'input100','placeholder':'Enter Username'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Enter Password'}))
 
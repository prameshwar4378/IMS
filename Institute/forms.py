
from django.contrib.auth.forms import UserCreationForm
from Developer.models import CustomUser,DB_Session
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.core.validators import RegexValidator


class CustomStaffCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','staff_profile','staff_name','email','staff_id_no','is_staff','password1','password2')


class Form_Financial_Year_Session(forms.ModelForm):
    financial_year = forms.CharField(
        max_length=7,
        validators=[RegexValidator(r'^\d{4}-\d{2}$', 'Enter a year in the format of "yyyy-yy".')]
    )
    class Meta:
        model = DB_Session
        fields = '__all__'


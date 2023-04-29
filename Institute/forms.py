
from django.contrib.auth.forms import UserCreationForm
from Developer.models import CustomUser,DB_Session
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.core.validators import RegexValidator

STATUS=(("Active","Active"),("Inactive","Inactive"))

class CustomStaffCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    status = forms.ChoiceField(choices=STATUS, initial='Active')
    class Meta:
        model = CustomUser
        fields = ('username','staff_profile','staff_name','email','staff_id_no','is_staff','status','password1','password2')
        widgets = { 
            'is_staff':forms.HiddenInput(),
        }
   
 
class CustomStaffUpdateForm(UserCreationForm):
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    status = forms.ChoiceField(choices=STATUS, initial='Active')
    class Meta:
        model = CustomUser
        fields = ('staff_profile','staff_name','email','staff_id_no','is_staff','status','password1','password2')
        widgets = { 
            'is_staff':forms.HiddenInput(),
        }
   
 
class Form_Financial_Year_Session(forms.ModelForm):
    financial_year = forms.CharField(
        max_length=7,
        validators=[RegexValidator(r'^\d{4}-\d{2}$', 'Enter a year in the format of "yyyy-yy".')]
    )
    class Meta:
        model = DB_Session
        fields = '__all__'


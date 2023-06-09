
from django.contrib.auth.forms import UserCreationForm
from Developer.models import CustomUser,DB_Session,DB_Fees,DB_Subjects
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.utils import timezone



FINANCIAL_YEAR = (
    ("2022-23", "2022-23"), 
    ("2023-24", "2023-24"), 
    ("2024-25", "2024-25"), 
    ("2025-26", "2025-26"), 
    ("2026-27", "2026-27"), 
    ("2028-28", "2028-28"), 
    
)   

class CustomStudentCreationForm(UserCreationForm):
    student_admission_date = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(attrs={'type': 'date'}))
    # academic_session_student=forms.ChoiceField(choices=FINANCIAL_YEAR, widget=forms.Select(attrs={'onchange': 'Call_Get_PRN_Function()', 'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('is_student','username','academic_session_student','student_profile','student_name','student_gender','student_dob','student_village','student_taluka','student_dist','parent_name','parent_mobile','parent_village','parent_taluka','parent_dist','student_collage','student_collage_address','batch','group','student_prn_no','student_admission_date','student_class','student_mobile','status','password1','password2')
        widgets = { 
            # 'academic_session_student': forms.ChoiceField(choices=FINANCIAL_YEAR,attrs={'onChange': 'Call_Get_PRN_Function()'}),
            'student_dob': forms.TextInput(attrs={'type': 'date'}),
            'student_name': forms.TextInput(attrs={'autofocus': True}),
        }
   
 

class FormStudentReceivedFees(forms.ModelForm):
    class Meta:
        model = DB_Fees
        fields = ('student_username','operator_username','operator_name','student_prn_no','student_name','student_class','received_remark','received_amount','amount_word','payment_mode','due_date','due_amount','due_remark')
        widgets={
            'student_prn_no':forms.HiddenInput(),
            'student_name':forms.HiddenInput(),
            'student_username':forms.HiddenInput(),
            'amount_word':forms.HiddenInput(),
            'operator_username':forms.HiddenInput(),
            'operator_name':forms.HiddenInput(),
            'received_date': forms.TextInput(attrs={'type': 'date'}),
            'due_date': forms.TextInput(attrs={'type': 'date'}),
            'received_amount': forms.TextInput(attrs={'onChange': 'numberToWord()'}),
        }
            
 

class FormAddFees(forms.ModelForm):
    class Meta:
        model = DB_Fees
        fields = ('add_fees','fees_remark','student_prn_no','student_username')
        widgets={
            'student_prn_no':forms.HiddenInput(), 
            'student_username':forms.HiddenInput(), 
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_prn_no'].widget.attrs.update({'id': 'id_student_prn_no_add_fees'})
        self.fields['student_username'].widget.attrs.update({'id': 'id_student_username_add_fees'})

 
# Education Session for Staff 
class Form_Academic_Session_Staff(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('academic_session_staff',)

 
# Education Session for Staff 
class Form_Subjects(forms.ModelForm):
    class Meta:
        model=DB_Subjects
        fields='__all__'

                
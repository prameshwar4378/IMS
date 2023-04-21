
from django.contrib.auth.forms import UserCreationForm
from Developer.models import CustomUser,DB_Session,DB_Fees,DB_Result,DB_Subjects,DB_Schedule_Exam,DB_Attendance
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
STUDENT_STATUS=(("Active","Active"),("Inactive","Inactive"))

class CustomStudentCreationForm(UserCreationForm):
    student_admission_date = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(attrs={'type': 'date'}))
    # academic_session=forms.ChoiceField(choices=FINANCIAL_YEAR, widget=forms.Select(attrs={'onchange': 'Call_Get_PRN_Function()', 'class': 'form-control'}))
    is_student = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    status = forms.ChoiceField(choices=STUDENT_STATUS, initial='Active')
    class Meta:
        model = CustomUser
        fields = ('is_student','username','academic_session','student_profile','student_name','student_gender','student_dob','student_village','student_taluka','student_dist','parent_name','parent_mobile','parent_village','parent_taluka','parent_dist','student_collage','student_collage_address','batch','group','student_prn_no','student_admission_date','student_class','student_mobile','status','password1','password2')
        labels = {
            'student_name': 'Full Name',
            'student_profile': 'Upload Profile Image',
            'student_gender': 'Gender',
            'student_dob': 'Date of Birth',
            'student_mobile': 'Mobile Number',
            'student_village': 'Village',
            'student_taluka': 'Taluka',
            'student_dist': 'Dist',
        }   
        widgets = { 
            # 'academic_session': forms.ChoiceField(choices=FINANCIAL_YEAR,attrs={'onChange': 'Call_Get_PRN_Function()'}),
            'student_dob': forms.TextInput(attrs={'type': 'date'}),
            'student_name': forms.TextInput(attrs={'autofocus': True}),
            'is_student':forms.HiddenInput(),
        }
   
 

class FormStudentReceivedFees(forms.ModelForm):
    class Meta:
        model = DB_Fees
        fields = ('academic_session','student_username','operator_username','operator_name','student_prn_no','student_name','student_class','received_remark','received_amount','amount_word','payment_mode','due_date','due_amount','due_remark')
        widgets={
            'academic_session':forms.HiddenInput(), 
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
        fields = ('academic_session','add_fees','fees_remark','student_prn_no','student_username')
        widgets={
            'academic_session':forms.HiddenInput(), 
            'student_prn_no':forms.HiddenInput(), 
            'student_username':forms.HiddenInput(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_prn_no'].widget.attrs.update({'id': 'id_student_prn_no_add_fees'})
        self.fields['student_username'].widget.attrs.update({'id': 'id_student_username_add_fees'})

 
# Education Session for Staff 
class Form_academic_session(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('academic_session',)

 
# Education Session for Staff 
class Form_Subject(forms.ModelForm):
    class Meta:
        model=DB_Subjects
        fields='__all__'


 
# Schedult Exam For Student
class Form_Schedule_Exam(forms.ModelForm):
    class Meta:
        model=DB_Schedule_Exam
        fields='__all__'
        widgets={
            'exam_start_date': forms.TextInput(attrs={'type': 'date'}),
            'exam_end_date': forms.TextInput(attrs={'type': 'date'}),
            'academic_session': forms.TextInput(attrs={'type': 'hidden'}),
        }
        def save(self, commit=True):
            instance = super().save(commit=False)
            # Get the session value using the request object from the form
            session_value = self.request.session.get('my_key')
            # Set the model field value to the session value
            instance.my_field = session_value
            if commit:
                instance.save()
            return instance


from datetime import date

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = DB_Attendance
        fields = ('id','student_prn_no', 'student_name', 'is_present')
        widgets={
            'student_prn_no': forms.TextInput(attrs={'class':'form-control'}),
            'student_name': forms.TextInput(attrs={'class':'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

 
class UpdateAttendanceForm(forms.ModelForm):
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DB_Attendance
        fields = ('id','student_prn_no', 'student_name', 'is_present')
        widgets={
            'id':forms.HiddenInput(), 
            'student_prn_no': forms.TextInput(attrs={'class':'form-control'}),
            'student_name': forms.TextInput(attrs={'class':'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

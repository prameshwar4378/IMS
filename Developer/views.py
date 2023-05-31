from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Custom_Institute_Creation_Form,login_form,Custom_Institute_Update_Form,Staff_Update_Form
from django.contrib import messages
from Institute.forms import CustomStaffCreationForm
from Developer.models import CustomUser,DB_Fees,DB_Attendance,DB_Result,DB_Schedule_Exam,DB_Web_Notification,DB_Subjects
import csv
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'login.html')
    else:
        return render(request,'index.html')


def developer_dashboard(request):
    return render(request,'developer_dashboard.html')



def login(request):
    lg_form=login_form() 
    rg_form=Custom_Institute_Creation_Form()
    if request.method=='POST':
        if 'txt_sign_in_username' in request.POST: 
            username = request.POST.get('txt_sign_in_username', False)
            password = request.POST.get('txt_sign_in_password', False)
            user=authenticate(request,username=username,password=password)

            if user is not None:
                dt=CustomUser.objects.get(username=username) 
                chek_profile_valid_or_not = CustomUser.objects.filter(is_institute=True,academic_session=dt.academic_session, institute_code=dt.institute_code).distinct()

                for i in chek_profile_valid_or_not:
                    valid_up_to_date = i.profile_valid_up_to

                if datetime.now().date() > valid_up_to_date:
                    profile_not_valid=True
                else:
                    profile_not_valid=False

                if profile_not_valid:
                    messages.info(request,"Profile Validity Expired Please Contact to Support Team")
                    return redirect('/accounts/login/')
                
                authlogin(request,user)
                if user.is_superuser==True:
                    return redirect('/Developer',{'user',user})
                elif user.is_institute==True:
                    return redirect('/Institute',{'user',user})
                elif user.is_staff==True:
                    return redirect('/Staff',{'user',user})
                elif user.is_student==True:
                    return redirect('/Student',{'user',user})
            else:
                lg_form=login_form()
                messages.warning(request,'Opps...! User does not exist... Please try again..!')


        if 'txt_sign_up_username' in request.POST:  
            username = request.POST.get('txt_sign_up_username', False)
            email = request.POST.get('txt_sign_up_email', False)
            password = request.POST.get('txt_sign_up_password', False)

            request.session['get_session_password']=request.POST.get('txt_sign_up_password'),
            
            profile_valid_upto = datetime.now() + timedelta(days=15)

            if len(username)<5:
                messages.info(request,'Username should atleast 5 characters')
                return redirect('/accounts/login/')

            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already exists!')
            else:
                create_user = CustomUser(
                    username=username,
                    email=email,
                    is_institute=True,
                    profile_valid_up_to=profile_valid_upto,
                    no_of_txt_sms=30
                )
                create_user.set_password(password)
                create_user.save() 
                messages.success(request,'Registration Successfully ...!')
                
                # Authenticate and login the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    authlogin(request, user)

                # Redirect the user to the appropriate page
                return redirect('/Institute/first_tour',{'user',user})
    return render(request,'login.html',{'form':lg_form,'rg_form':rg_form})




def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')



def institute_details_dashboard(request,id):
    dt = get_object_or_404(CustomUser, id=id)
    institute_code=dt.institute_code
    Fees_Records=DB_Fees.objects.filter(academic_session=request.user.academic_session,institute_code=institute_code)
    Students=CustomUser.objects.filter(academic_session=request.user.academic_session,institute_code=institute_code,is_student=True).count()
    Subjects=DB_Subjects.objects.filter(institute_code=institute_code).count()
    Exams=DB_Schedule_Exam.objects.filter(academic_session=request.user.academic_session,institute_code=institute_code).count()
    Web_Notification=DB_Web_Notification.objects.filter(academic_session=request.user.academic_session,institute_code=institute_code).count()

    
    total_fees=0
    collected_fees=0 
    pending_dues=0  
    for i in Fees_Records:
        if i.add_fees != None:
            total_fees+=i.add_fees
        if i.received_amount != None:
            collected_fees += int(i.received_amount)
        if i.due_amount != None:
            pending_dues += int(i.due_amount)
            print("Due Amount is",i.due_amount)
 
    total_pending=total_fees - collected_fees    
    contaxt={
        "institute_address":dt.institute_address,
        "institute_name":dt.institute_name,
        "total_fees":total_fees,
        "collected_fees":collected_fees,
        "pending_dues":pending_dues,
        "total_pending":total_pending,
        "total_students":Students,
        "total_subjects":Subjects,
        "total_exam_scheduled":Exams,
        "web_notifications":Web_Notification
             }
    return render(request,"developer__institute_details_dashboard.html",contaxt)


from django.contrib.auth.forms import SetPasswordForm
def update_institute_password(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request,'Password Updated Succesfully')
            return redirect('/Developer/institute_list/')
    else:
        form = SetPasswordForm(user=user)
    return render(request, 'developer__update_institute_password.html', {'form': form})

def update_staff_password(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request,'Password Updated Succesfully')
            return redirect('/Developer/staff_list/')
    else:
        form = SetPasswordForm(user=user)
    return render(request, 'developer__update_staff_password.html', {'form': form})


def institute_list(request):
    rec=CustomUser.objects.filter(is_institute=True)
    return render(request,'institute_list.html', {'rec': rec})

def staff_list(request):
    rec=CustomUser.objects.filter(is_staff=True)
    return render(request,'developer__staff_list.html', {'rec': rec})

import time
def add_institute(request):
    if request.method == 'POST':
        form = Custom_Institute_Creation_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Institute Added Successfully ...!')
            return redirect('/Developer/add_institute/')
    else:
        form = Custom_Institute_Creation_Form()
    return render(request, 'add_institute.html', {'form': form})
 
def update_institute(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Custom_Institute_Update_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Institute Updated Successfully')
            return redirect('/Developer/institute_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Custom_Institute_Update_Form(instance=pi)
    return render(request,'update_institute.html',{'form':fm})

 
def update_staff(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Staff_Update_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Staff Updated Successfully')
            return redirect('/Developer/staff_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Staff_Update_Form(instance=pi)
    return render(request,'developer__update_staff.html',{'form':fm})

            
 
def delete_institute(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Institute Deleted Successfully!!!')
        return redirect('/Developer/institute_list/')


def delete_staff(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Staff Deleted Successfully!!!')
        return redirect('/Developer/staff_list/')


def import_export(request):
    if request.method == "POST":  
        if 'institute_import' in request.FILES: 
            csv_file = request.FILES['institute_import']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            for i in decoded_file:
                print(i)
            reader = csv.DictReader(decoded_file)
            for row in reader:
                try:
                    CustomUser.objects.create(
                        username=row['username'],
                        academic_session=row['academic_session'],
                        institute_name=row['institute_name'],
                        institute_address=row['institute_address'],
                        institute_code=row['institute_code']
                    )
                except Exception as e:
                    return redirect('/')
                
    return render(request,'import_export.html')




from django.db.models import Count

def error_list(request):
    profile_data=CustomUser.objects.all()
    duplicate_records = CustomUser.objects.values('institute_code', 'is_institute').annotate(count=Count('id')).filter(count__gt=1)
    for record in duplicate_records:
        print(f"Institute Code: {record['institute_code']}, Is Institute: {record['is_institute']}")
    return render(request,'error_list.html')
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CustomStudentCreationForm,Form_Academic_Session_Staff,Form_Subject,Form_Schedule_Exam
from Developer.models import CustomUser,DB_Fees,DB_Session,DB_Result,DB_Subjects,DB_Schedule_Exam
from Staff.forms import FormStudentReceivedFees,FormAddFees
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.db.models import Q
from .filters import DueFees_Filter,Student_name_Filter
from . import export
# Create your views here.

def update_education_session(request):
    name=request.user.username
    
    user = CustomUser.objects.get(username=name)
    user.academic_session_staff = '2022-23'
    user.save()
    fm=Form_Academic_Session_Staff()
    if request.method == 'POST':
            my_field_value = request.POST.get('academic_session_staff')
            user.academic_session_staff = my_field_value
            user.save()
            messages.success(request, 'Session Updated Success...!.')
            return redirect('/Staff')

    contaxt={'name':name,'form':fm}
    return render(request,'update_education_session.html',contaxt)

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def home(request):
    return render(request,'staff_dashboard.html')

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_list(request):
    rec=CustomUser.objects.filter(is_student=True)
    return render(request,'student_list.html',{'rec':rec})

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def new_admission(request):
    session_student=request.user.academic_session_staff
    record=CustomUser.objects.filter(academic_session_student=session_student,is_student=True)
    student_count=str(record.count()+1)

    split_session1=session_student[-5:-3]
    split_session2=session_student[-2:]
    prn_no=split_session1+split_session2+str(0)+student_count

    if request.method == 'POST':
        form = CustomStudentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Success...!.')
            form = CustomStudentCreationForm()
            return redirect('/Staff/new_admission/')
    else:
        form = CustomStudentCreationForm()
    return render(request,'admission_form.html', {'form': form,'academic_session_student':session_student,'auto_prn':prn_no})


# Student dashboard
# Add fees form
def student_panel(request):
    active_students=CustomUser.objects.filter(is_student=True).count()
    due_records=DB_Fees.objects.exclude(Q(due_amount__isnull=True) | Q(due_amount=0)).count()
    context={'active_students':active_students,'due_records':due_records}
    return render(request,'student_panel.html',context)



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_dashboard(request,id):
    dt=get_object_or_404(CustomUser,id=id)
    prn_no=dt.student_prn_no
    rec = DB_Fees.objects.filter(student_prn_no=prn_no)

    total_fees=0
    collected_fees=0 
    pending_dues=0  
    for i in rec:
        if i.add_fees != None:
            total_fees+=i.add_fees
        if i.received_amount != None:
            collected_fees += int(i.received_amount)
        if i.due_amount != None:
            pending_dues += int(i.due_amount)
            print("Due Amount is",i.due_amount)
        
        # pending_fees=int(total_admission_fees)-int(total_collected_fees)
    # else:
    #     total_admission_fees=0
    #     pending_fees=0
 
    total_pending=total_fees - collected_fees
    


    form_receive_fees = FormStudentReceivedFees()
    form_add_fees = FormAddFees()

    if request.method == 'POST':
        if 'received_amount' in request.POST:
            form_receive_fees = FormStudentReceivedFees(request.POST)
            if form_receive_fees.is_valid():
                form_receive_fees.save()
                messages.success(request, 'Fees Received Successfully...!')
                form_receive_fees = FormStudentReceivedFees()
                return redirect(f'/Staff/student_dashboard/{id}')
        
        elif 'add_fees' in request.POST:
            form_add_fees = FormAddFees(request.POST)
            if form_add_fees.is_valid():
                form_add_fees.save()
                messages.success(request, 'Fees Added Successfully...!')
                form_add_fees = FormAddFees()
                return redirect(f'/Staff/student_dashboard/{id}')
    else:
        form_receive_fees = FormStudentReceivedFees()
        form_add_fees = FormAddFees()

    context ={'fees_form':form_receive_fees,'add_fees_form':form_add_fees,'data':dt,'fees_rec':rec,'total_fees':total_fees,'collected_fees':collected_fees,'pending_dues':pending_dues,'total_pending':total_pending}

    return render(request,"student_dashboard.html",context )




@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def update_student_profile(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStudentCreationForm(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('/Staff/new_admission/')

        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStudentCreationForm(instance=pi)
    return render(request,'update_student_profile.html',{'form':fm})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_student(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Profile Deleted Successfully!!!')
        return redirect('/Staff/student_list/')



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_fees_record(request,id):
        dt=get_object_or_404(DB_Fees,id=id)
        user=dt.student_username
        var_username = CustomUser.objects.get(username=user)
        student_id=var_username.id
        pi=DB_Fees.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Record Deleted Successfully!!!')
        return redirect(f'/Staff/student_dashboard/{student_id}')
        

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def print_admission_form(request,id):
    dt=get_object_or_404(CustomUser,id=id)
    return render(request,"print_admission_form.html",{'id':id,'data':dt})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def print_fees_receipt(request,id):
    dt=get_object_or_404(DB_Fees,id=id)
    return render(request,"print_fees_receipt.html",{'data':dt})


def due_list(request):
    due_records=DB_Fees.objects.exclude(Q(due_amount__isnull=True) | Q(due_amount=0))
    Filter=DueFees_Filter(request.GET, queryset=due_records)
    rec2=Filter.qs 
    total_students=rec2.count()
    total_value = rec2.aggregate(Sum('due_amount'))
    total_due_amount = str(total_value['due_amount__sum'])
    context={'rec':rec2,'filter':Filter,'total_students':total_students,'total_due_amount':total_due_amount}
    return render(request,"due_list.html",context)

def due_update(request,id):
    if request.method=="POST":
        pi=DB_Fees.objects.get(pk=id)
        fm=FormStudentReceivedFees(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Fees Updated Successfully')
            return redirect('/Staff/due_list/')

        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=DB_Fees.objects.get(pk=id)
        fm=FormStudentReceivedFees(instance=pi)
    return render(request,"update_due_record.html",{'form':fm})

from . import export
def export_pdf_deu_records(request):
    responce = export.export_pdf_due(request)
    return responce


def export_excel_deu_records(request):
    responce = export.export_excel_deu()
    return responce

def manage_subjects(request):
    rec=DB_Subjects.objects.all()
    form=Form_Subject()
    if request.method=="POST":
        form=Form_Subject(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Subject Added Successfully')
            form=Form_Subject()
            return redirect('/Staff/manage_subjects/')
    else:
        form=Form_Subject()
    context={'form':form,'rec':rec}
    return render(request,'subjects.html',context)


def delete_subject(request,id):
        pi=DB_Result.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Subject Deleted Successfully!!!')
        return redirect('/Staff/manage_subjects/')
 
def student_result_dashboard(request,id):
    student_profile_record=CustomUser.objects.get(id=id)
    result_record=DB_Result.objects.filter(student_prn_no=student_profile_record.student_prn_no)
    exam_name = DB_Schedule_Exam.objects.filter(class_name=student_profile_record.student_class).order_by('-id')

    # student_name=student_record.student_name
    if request.method == 'POST':
        # Get data from POST request
        if 'add_result' in request.POST: 
            student_prn_no = request.POST.get('student_prn_no')
            subject_name = request.POST.get('subject_name')
            min_marks = request.POST.get('min_marks')
            obtained_marks = request.POST.get('obtained_marks')
            out_off_marks = request.POST.get('out_off_marks')
            percentage = request.POST.get('percentage')
            result = request.POST.get('result')
            exam_data = request.POST.get('cmb_exam_name')
            exam_title, exam_start_date, exam_end_date = exam_data.split(" | ")

            save_result = DB_Result(
                student_prn_no=student_prn_no,
                subject_name=subject_name,
                min_marks=min_marks,
                obtained_marks=obtained_marks,
                out_off_marks=out_off_marks,
                percentage=percentage,
                result=result,
                exam_title=exam_title,
                exam_start_date=exam_start_date,
                exam_end_date=exam_end_date
            )
            save_result.save()
            messages.success(request,'Marks Added Successfully!!!')
        elif 'txt_update_result_id' in request.POST: 
            result_id = request.POST.get('txt_update_result_id')
            update_exam_data = request.POST.get('cmb_update_exam_name')
            update_exam_title, update_exam_start_date, update_exam_end_date = update_exam_data.split(" | ")
        
            # Select the record with the given ID and update its fields
            DB_Result.objects.filter(id=result_id).update(
                student_prn_no=request.POST.get('txt_update_student_prn_no'),
                subject_name=request.POST.get('cmb_update_subject_name'),
                min_marks=request.POST.get('txt_update_min_marks'),
                obtained_marks=request.POST.get('txt_update_obtained_marks'),
                out_off_marks=request.POST.get('txt_update_out_off_marks'),
                percentage=request.POST.get('txt_update_percentage'),
                result=request.POST.get('txt_update_result'),
                exam_title=update_exam_title,
                exam_start_date=update_exam_start_date,
                exam_end_date=update_exam_end_date
            )
            messages.success(request, 'Marks Updated Successfully!!!')
        elif 'report_type' in request.POST:
            report_type=request.POST.get('report_type')
            if report_type == "Subject Wise":
                pass
            elif report_type == "Exam Wise":
                exam_name=request.POST.get('select_exam_for_report')
                print(exam_name)
                

    labels = []
    data_chart = []
    if result_record.count() != 0:
        for i in result_record:
            labels.append(str(i.subject_name))
            data_chart.append(int(i.obtained_marks))
 
    subjects=DB_Subjects.objects.filter(class_name=student_profile_record.student_class)
    context={'subject_name':subjects,'st_data':student_profile_record,'result_record':result_record,'exam_record':exam_name,'labels':labels,'data':data_chart}
    return render(request,'student_result_dashboard.html',context)



def delete_result(request,id):
        pi=DB_Result.objects.get(pk=id)

        id_for_page_redirect=CustomUser.objects.get(student_prn_no=pi.student_prn_no).id
        pi.delete()
        messages.success(request,'Result Deleted Successfully!!!')
        return redirect(f'/Staff/student_result_dashboard/{id_for_page_redirect}')
 

def schedule_exam(request):
    rec=DB_Schedule_Exam.objects.all()
    form=Form_Schedule_Exam()
    if request.method=="POST":
        form=Form_Schedule_Exam(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Exam Created Successfully')
            form=Form_Schedule_Exam()
            return redirect('/Staff/schedule_exam/')
    else:
        form=Form_Schedule_Exam()
    context={'form':form,'rec':rec}
    return render(request,'schedule_exam.html',context)


def delete_exam_schedule(request,id):
        pi=DB_Schedule_Exam.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Exam  Deleted Successfully!!!')
        return redirect('/Staff/schedule_exam/')
 
from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from Developer.models import DB_Fees,DB_Attendance,DB_Result,DB_Schedule_Exam,CustomUser,DB_Subjects
from Staff.filters import Attendance_Filter
from django.db.models import Sum
# Create your views here.
def student_dashboard(request):
    PRN_NO=request.user.student_prn_no
    CLASS_NAME=request.user.student_class 

    dt=get_object_or_404(CustomUser,student_prn_no=PRN_NO)
 
    fees_rec = DB_Fees.objects.filter(student_prn_no=PRN_NO)

    total_fees=0
    paid_fees=0 
    pending_dues=0  
    for i in fees_rec:
        if i.add_fees != None:
            total_fees+=i.add_fees
        if i.received_amount != None:
            paid_fees += int(i.received_amount)
        if i.due_amount != None:
            pending_dues += int(i.due_amount)
    pending_fees=int(total_fees)-int(paid_fees)
    

    
    exam_schedule_records=DB_Schedule_Exam.objects.filter(class_name=CLASS_NAME).last()
    if exam_schedule_records:
        exam_name_for_result_chart = f"{exam_schedule_records.exam_title} ({exam_schedule_records.exam_start_date} To {exam_schedule_records.exam_end_date})"
    else:
        exam_name_for_result_chart=""
    if exam_schedule_records:
        result_records=DB_Result.objects.filter(exam_title=exam_schedule_records.exam_title)
    else:
        result_records=""
    label_subject_name_result=[]
    data_marks_result=[]
    for i in result_records:
        if i.subject_name in label_subject_name_result:
            subject_index_value=label_subject_name_result.index(i.subject_name)
            data_marks_result[subject_index_value]+=int(i.obtained_marks)
        else:
            label_subject_name_result.append(i.subject_name)
            data_marks_result.append(int(i.obtained_marks)) 

    subject_marks_rec=DB_Result.objects.filter(student_prn_no=PRN_NO)
    label_subject_name_progress=[]
    data_marks_progress=[]
    total_out_of=[]
    for i in subject_marks_rec:
        if i.subject_name in label_subject_name_progress:
            subject_index_value=label_subject_name_progress.index(i.subject_name)
            data_marks_progress[subject_index_value]+=int(i.obtained_marks)
            total_out_of[subject_index_value]+=int(i.out_off_marks)
        else:
            label_subject_name_progress.append(i.subject_name)
            data_marks_progress.append(int(i.obtained_marks)) 
            total_out_of.append(int(i.out_off_marks)) 

    average_marks=[]
    for i in range(len(data_marks_progress)):
        percentage = (float(data_marks_progress[i]) / float(total_out_of[i])) * 100
        average_marks.append(percentage)
        
    print(label_subject_name_progress)
    print(data_marks_progress)
    print(total_out_of)
    print(average_marks)

    contaxt={'total_fees':total_fees,
             'paid_fees':paid_fees,
             'pending_fees':pending_fees,
             'exam_name_for_result_chart':exam_name_for_result_chart,
             'label_subject_name_result':label_subject_name_result,
             'data_marks_result':data_marks_result,
             'label_subject_name_progress':label_subject_name_progress,
             'average_marks_for_progress':average_marks,
             }    
    return render(request,'student__student_dashboard.html',contaxt)

def attendance(request):
    attendance_records=DB_Attendance.objects.filter(student_class=request.user.student_class,student_prn_no=request.user.student_prn_no,academic_session=request.user.academic_session) 
    print(attendance_records) 

    Filter=Attendance_Filter(request.GET, queryset=attendance_records)
    filtered_rec=Filter.qs

    Filter1=Attendance_Filter(request.GET, queryset=attendance_records)
    filter_total_attendance_rec=Filter1.qs
    total_attendance_count=Filter1.qs.count()

    Filter2=Attendance_Filter(request.GET, queryset=attendance_records.filter(is_present=True))
    present_rec_count=Filter2.qs.count()
    
    Filter3=Attendance_Filter(request.GET, queryset=attendance_records.filter(is_present=False))
    absent_rec_count=Filter3.qs.count()

    labels_charts = ['Present','Absent']
    data_charts = [present_rec_count,absent_rec_count]

    if total_attendance_count > 0:
        percentage=(present_rec_count/total_attendance_count)*100
    else:
        percentage=0

    context={
        'total_attendance_count':total_attendance_count,
        'present_rec_count':present_rec_count,
        'absent_rec_count':absent_rec_count,
        'labels_charts':labels_charts,
        'data_charts':data_charts,
        'filter':Filter,
        'filter_total_attendance_rec':filtered_rec,
        'percentage':percentage
    }
    return render(request,"student__student_attendance.html",context)

def student_due(request):
    due_records=DB_Fees.objects.filter(due_amount__isnull=False, due_amount__gt=0,student_class=request.user.student_class,student_prn_no=request.user.student_prn_no, academic_session=request.user.academic_session)
    total_value = due_records.aggregate(Sum('due_amount'))
    total_due_amount = str(total_value['due_amount__sum'])
    context={'rec':due_records,'total_due_amount':total_due_amount}
    return render(request,"student__due_list.html",context)

def student_fees(request):
    fees_rec=DB_Fees.objects.filter(student_class=request.user.student_class,student_prn_no=request.user.student_prn_no, academic_session=request.user.academic_session)
    print(fees_rec.count())
    context={'fees_rec':fees_rec}
    return render(request,"student__fees_dashboard.html",context)

from Staff import export
def result_dashboard(request):
    PRN_NO=request.user.student_prn_no
    result_record=DB_Result.objects.filter(student_prn_no=PRN_NO,academic_session=request.user.academic_session)
    exam_name = DB_Schedule_Exam.objects.filter(class_name=request.user.student_class,academic_session=request.user.academic_session).order_by('-id')

    if request.POST:
        report_type=request.POST.get('report_type')
        if report_type == "Subject Wise":
            subject_name_1=request.POST.get('select_subject_for_report')
            student_prn_no=PRN_NO
            responce = export.export_result_report_subject_wise(subject_name_1,student_prn_no)
            return responce

        elif report_type == "Exam Wise":
            exam_name_1=request.POST.get('select_exam_for_report')
            title_1, start_date_1, end_date_1 = exam_name_1.split(" | ")
            st_name=request.user.student_name
            st_prn=PRN_NO

            result_data = DB_Result.objects.filter(exam_title=title_1,exam_start_date=start_date_1,exam_end_date=end_date_1,student_prn_no=PRN_NO)
            
            if result_data:
                student_class = result_data.first().student_class
                st_class=student_class


            labels_charts = []
            data_charts = []
            st_total_obtained=0
            st_total_out_off=0
            st_total_min=0
            st_result=[]
            for i in result_data:
                labels_charts.append(i.subject_name)
                data_charts.append(i.obtained_marks)
                st_total_obtained+=int(i.obtained_marks)
                st_total_out_off+=int(i.out_off_marks)
                st_total_min+=int(i.min_marks)
                st_result.append(i.result)

            if "Fail" in st_result:
                st_result="Fail"
            else:
                st_result="Pass"

            if st_total_out_off >0:
                st_percentage=(st_total_obtained/st_total_out_off)*100
            else:
                st_percentage="---"
                
            st_profile=request.user.student_profile
            institute_name=request.user.institute_name
            institute_logo=request.user.institute_logo
            institute_address=request.user.institute_address


            context={'rec':result_data,
                        'st_profile':st_profile,
                        'st_name':st_name,
                        'institute_name':institute_name,
                        'institute_logo':institute_logo,
                        'institute_address':institute_address,
                        'st_prn':st_prn,
                        'st_class':st_class,
                        'exam_title':title_1,
                        'exam_start_date':start_date_1,
                        'exam_end_date':end_date_1,
                        'st_total_min':st_total_min,
                        'st_total_obtained':st_total_obtained,
                        'st_total_out_off':st_total_out_off,
                        'st_percentage':st_percentage,
                        'st_result':st_result,
                        'labels_charts':labels_charts,
                        'data_charts':data_charts,
                        }
            
            return render(request,'staff__print_result_exam_wise.html',context)
    labels = []
    data_chart = []
    if result_record.count() != 0:
        for i in result_record:
            if i.subject_name not in labels:
                labels.append(str(i.subject_name))
            index_val=labels.index(i.subject_name)
            if index_val < len(data_chart):
                data_chart[index_val]=data_chart[index_val]+int(i.obtained_marks)
            else:
                data_chart.append(int(i.obtained_marks))

    subjects=DB_Subjects.objects.filter(class_name=request.user.student_class)

    context={'result_record':result_record,'exam_record':exam_name,'subject_name':subjects,'labels':labels,'data':data_chart}
    return render(request,"student__result_dashboard.html",context)
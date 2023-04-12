from Developer.models import DB_Fees
from .filters import DueFees_Filter
from django.template.loader import get_template
from django.db.models import Sum,Q
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa 
import csv


def export_pdf_due(request): 
    template = get_template('export_pdf_due_records.html')
    due_records=DB_Fees.objects.exclude(Q(due_amount__isnull=True) | Q(due_amount=0))
    Filter=DueFees_Filter(request.GET, queryset=due_records)
    rec2=Filter.qs 
    total_value = rec2.aggregate(Sum('due_amount'))
    total_due_amount = str(total_value['due_amount__sum'])
    context={'rec':rec2,'total_due_amount':total_due_amount}
  
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Due Records.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)


def export_excel_deu():
    responce=HttpResponse(content_type='text/csv')
    writer=csv.writer(responce)
    writer.writerow(['student_prn_no','student_name','student_class','received_date','payment_mode','received_amount','received_remark','due_date','due_amount','due_remark'])
    for data in DB_Fees.objects.filter(due_amount__isnull=False).values_list('student_prn_no','student_name','student_class','received_date','payment_mode','received_amount','received_remark','due_date','due_amount','due_remark'):
       writer.writerow(data)    
    responce['Content-Disposition'] = 'attachment; filename="Student Due Records.csv"'
    return responce

def export_result_report_exam_wise(request):
    pass



from django.urls import path
from Staff import views as Staff_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', Staff_view.home,name="staff_dashboard"),  
    path('student_list/', Staff_view.student_list,name="student_list"), 
    path('new_admission/', Staff_view.new_admission,name="new_admission"),  
    path("student_panel/",Staff_view.student_panel, name='student_panel'),  
    path("student_dashboard/<int:id>",Staff_view.student_dashboard, name='student_dashboard'), 
    path("print_admission_form/<int:id>",Staff_view.print_admission_form, name='print_admission_form'), 
    path("print_fees_receipt/<int:id>",Staff_view.print_fees_receipt, name='print_fees_receipt'),  
    path("update_student_profile/<int:id>",Staff_view.update_student_profile, name='update_student_profile'), 
    path("delete_student/<int:id>",Staff_view.delete_student, name='delete_student'), 
    path("delete_fees_record/<int:id>",Staff_view.delete_fees_record, name='delete_fees_record'), 
    path('due_list/', Staff_view.due_list, name='due_list'),
    path('due_update/<int:id>', Staff_view.due_update, name='due_update'),
    path('update_education_session/', Staff_view.update_education_session, name='update_education_session'),
    path('export_pdf_deu_records/', Staff_view.export_pdf_deu_records, name='export_pdf_deu_records'),
    path('export_excel_deu_records/', Staff_view.export_excel_deu_records, name='export_excel_deu_records'),
    path('manage_subjects/', Staff_view.manage_subjects, name='manage_subjects'),
    path('delete_subject/<int:id>', Staff_view.delete_subject, name='delete_subject'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
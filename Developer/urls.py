
from django.urls import path
from Developer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.developer_dashboard,name="developer_dashboard"),
    path('institute_list/', views.institute_list,name="developer_institute_list"),
    path('staff_list/', views.staff_list,name="developer_staff_list"),
    path('add_institute/', views.add_institute,name="add_institute"),
    path('delete_institute/<int:id>', views.delete_institute,name="delete_institute"),
    path('delete_staff/<int:id>', views.delete_staff,name="developer__delete_staff"),
    path('update_institute/<int:id>', views.update_institute,name="update_institute"),
    path('update_institute_password/<int:id>', views.update_institute_password,name="update_institute_password"),
    path('import_export/', views.import_export,name="import_export"),
    path('error_list/', views.error_list,name="error_list"),
    path('update_staff/<int:id>', views.update_staff,name="developer__update_staff"),
    path('update_staff_password/<int:id>', views.update_staff_password,name="update_staff_password"),
    path('institute_details_dashboard/<int:id>', views.institute_details_dashboard,name="institute_details_dashboard"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

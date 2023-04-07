
from django.urls import path
from Institute import views as Institute_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Institute_view.home,name="institute_dashboard"),  
    path('staff_list/', Institute_view.staff_list,name="staff_list"), 
    path('add_staff/', Institute_view.add_staff,name="add_staff"),  
    path('manage_session/', Institute_view.manage_session,name="manage_session"),   
    path('update_session/<int:id>', Institute_view.update_session,name="update_session"),   
    path('delete_session/<int:id>', Institute_view.delete_session,name="delete_session"),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    
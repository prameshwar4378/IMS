
from django.urls import path
from Developer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('institute_list/', views.institute_list,name="institute_list"),
    path('add_institute/', views.add_institute,name="add_institute"),
    path('delete_institute/<int:id>', views.delete_institute,name="delete_institute"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

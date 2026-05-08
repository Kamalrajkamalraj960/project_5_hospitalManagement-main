from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),     
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('booking/', views.booking, name='booking'),
    path('login/', views.user_login, name='login'),
    path('patient-signup/', views.patient_signup, name='patient_signup'),
    path('doctor-signup/', views.doctor_signup, name='doctor_signup'),
    path('view-reports/', views.view_reports, name='view_reports'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('logout/', views.user_logout, name='logout'),
    
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),

    
]   
  
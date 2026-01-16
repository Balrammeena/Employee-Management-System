from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),

    path('add/', views.add_employee, name='add_employee'),
    path('update/<int:id>/', views.update_employee, name='update_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),

    # NEW PAGES (buttons)
    path('messages/', views.messages_page, name='messages'),
    path('employee/settings/', views.employee_settings, name='employee_settings'),
    path('employee/recall/', views.employee_recall, name='employee_recall'),
    path('employee/reports/', views.reports_page, name='reports'),

    # Export
    path('export/', views.export_employees_csv, name='export_employees'),
]

from django.urls import path
from . import views

urlpatterns = [
    # General / Auth
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Trainer
    path('trainer/signup/', views.trainer_signup, name='trainer_signup'),
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/workload/add/', views.add_workload, name='add_workload'),
    path('trainer/invoice/raise/', views.raise_invoice, name='raise_invoice'),
    path('trainer/invoice/<int:invoice_id>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('trainer/profile/update/', views.update_trainer_profile, name='update_trainer_profile'),
    
    # Admin - Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin - Trainer Controls
    path('admin/trainer/<int:trainer_id>/', views.admin_view_trainer, name='admin_view_trainer'),
    path('admin/trainer/<int:trainer_id>/toggle-status/', views.admin_toggle_trainer_status, name='admin_toggle_trainer_status'),
    path('admin/trainer/<int:trainer_id>/project/<int:project_id>/report/', views.admin_download_project_report, name='admin_download_project_report'),
    
    # Admin - Project Controls
    path('admin/project/add/', views.admin_add_project, name='admin_add_project'),
    path('admin/project/<int:project_id>/edit/', views.admin_edit_project, name='admin_edit_project'),
    path('admin/project/<int:project_id>/toggle-status/', views.admin_toggle_project_status, name='admin_toggle_project_status'),
    
    # Admin - Expenses
    path('admin/expense/add/', views.admin_add_expense, name='admin_add_expense'),
    path('admin/expense/download-excel/', views.admin_download_expenses_excel, name='admin_download_expenses_excel'),
    
    # Admin - Invoices
    path('admin/invoice/<int:invoice_id>/update-status/', views.admin_update_invoice_status, name='admin_update_invoice_status'),
]

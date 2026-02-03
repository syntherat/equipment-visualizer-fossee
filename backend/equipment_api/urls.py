from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_csv, name='upload'),
    path('summary/<int:dataset_id>/', views.get_summary, name='summary'),
    path('history/', views.get_history, name='history'),
    path('report/<int:dataset_id>/', views.generate_pdf_report, name='report'),
    path('health/', views.health_check, name='health'),
]

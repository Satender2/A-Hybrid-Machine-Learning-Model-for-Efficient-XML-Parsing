from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('parsers/', views.parser_management, name='parser_management'),
    path('parsers/edit/<int:pk>/', views.edit_parser, name='edit_parser'),
    path('parsers/delete/<int:pk>/', views.delete_parser, name='delete_parser'),
    path('training/', views.training_management, name='training'),
    path('training/train/', views.train_model, name='train_model'),
    path('logs/', views.system_logs, name='logs'),
]

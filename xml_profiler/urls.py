from django.urls import path
from . import views

app_name = 'xml_profiler'

urlpatterns = [
    path('upload/', views.upload_xml, name='upload'),
    path('optimize/<int:pk>/', views.optimize_parser, name='optimize'),
    path('result/<int:pk>/', views.parsing_result, name='result'),
    path('download/<int:pk>/', views.download_code, name='download_code'),
    path('history/', views.upload_history, name='history'),
    path('delete/<int:pk>/', views.delete_upload, name='delete'),
]

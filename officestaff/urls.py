from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students-detail/', StudentDetailView.as_view(), name='student-detail-by-custom-id'),
    path('fees_history-detail/', FeeHistoryDetailView.as_view(), name='fees-history-detail'),
    path('fees_history/', FeeHistoryListCreateView.as_view(), name='fees-history-list-create'),
   
   
 
    
    
    

    
]
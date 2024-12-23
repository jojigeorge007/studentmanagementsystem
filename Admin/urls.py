from django.urls import path
from .views import *

urlpatterns = [
    path('create_officestaff/', OfficeStaffCreateView.as_view(), name='office-staff-rcreate'),
    path('officestaff_list/', OfficeStaffListView.as_view(), name='office-staff-list'),
    path('officestaff_update/', OfficeStaffUpdateView.as_view(), name='office-staff-update'),
    path('officestaff_delete/', OfficeStaffDeleteView.as_view(), name='office-staff-delete'),
    path('create_librarian/',LibrarianCreateView.as_view(), name='create-librarian'),
    path('librarian_list/', LibrarianListView.as_view(), name='librarian-list'),
    path('librarian-update/', LibrarianUpdateView.as_view(), name='librarian-update'),
    path('librarian-delete/', LibrarianDeleteView.as_view(), name='librarian-delete'),
    path('students-create/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/detail/', StudentDetailView.as_view(), name='student-detail'),
   
    

 
    
]
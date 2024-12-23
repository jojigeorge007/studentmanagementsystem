from django.urls import path
from .views import *
urlpatterns = [
    path('library/history/', LibraryHistoryView.as_view(), name='library_history'),
    
    
    

    
]
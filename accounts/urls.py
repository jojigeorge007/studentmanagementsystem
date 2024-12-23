
from django.urls import include, path
from .views import *


urlpatterns = [path('login/', CustomLoginView.as_view(), name='custom-login'),
            
]

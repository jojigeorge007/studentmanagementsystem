
from django.contrib import admin
from accounts.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(OfficeStaff)
admin.site.register(Librarian)
admin.site.register(Country_Codes)
admin.site.register(State)
admin.site.register(Student)
admin.site.register(District)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)

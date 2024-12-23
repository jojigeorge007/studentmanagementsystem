from rest_framework import serializers
from accounts.models import *

# Create your views here.
class AddOfficeStaffSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    landmark = serializers.CharField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    country_code = serializers.PrimaryKeyRelatedField(queryset=Country_Codes.objects.all())  
    
    password = serializers.CharField(write_only=True, required=True)


    photo = serializers.ImageField(required=False)
    verification_id = serializers.CharField(required=False)
    verificationid_number = serializers.CharField(required=False)
    id_copy = serializers.FileField(required=False)
    status = serializers.ChoiceField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')],required=False)

    class Meta:
        model = OfficeStaff
        fields = ['email','phone_number','full_name','address','pin_code','district','landmark','country_code',
                  'state','country_code','photo','verification_id','verificationid_number','id_copy','status','password']
        
    

class AddLibrarianSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    landmark = serializers.CharField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    country_code = serializers.PrimaryKeyRelatedField(queryset=Country_Codes.objects.all())  
    
    password = serializers.CharField(write_only=True, required=True)


    photo = serializers.ImageField(required=False)
    verification_id = serializers.CharField(required=False)
    verificationid_number = serializers.CharField(required=False)
    id_copy = serializers.FileField(required=False)
    status = serializers.ChoiceField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')],required=False)

    class Meta:
        model = Librarian
        fields = ['email','phone_number','full_name','address','pin_code','district','landmark','country_code',
                  'state','country_code','photo','verification_id','verificationid_number','id_copy','status','password']
        



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'date_of_birth', 'admission_number', 'custom_id', 
            'photo', 'gender', 'class_level', 'admission_date', 'address', 'id_document', 
            'id_number', 'id_proof_file', 'status', 'guardian_name', 'guardian_relation', 
            'guardian_number', 'created_date'
        ]
class OfficeStaffSerializer(serializers.ModelSerializer):
    # Access User fields
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    place = serializers.CharField(source='user.place', read_only=True)
    pin_code = serializers.CharField(source='user.pin_code', read_only=True)
    district = serializers.CharField(source='user.district.name', read_only=True)
    state = serializers.CharField(source='user.state.name', read_only=True)
    joining_date = serializers.DateField(source='user.joining_date', read_only=True)
    
    class Meta:
        model = OfficeStaff
        fields = [
            'custom_id', 'photo', 'id_copy', 'status', 'verification_id', 'verificationid_number', 'created_date',
            'full_name', 'email', 'phone_number', 'address', 'place', 'pin_code', 'district', 'state', 'joining_date'
        ]


class LibrarianSerializer(serializers.ModelSerializer):
    # Access User fields
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    place = serializers.CharField(source='user.place', read_only=True)
    pin_code = serializers.CharField(source='user.pin_code', read_only=True)
    district = serializers.CharField(source='user.district.name', read_only=True)
    state = serializers.CharField(source='user.state.name', read_only=True)
    joining_date = serializers.DateField(source='user.joining_date', read_only=True)
    
    class Meta:
        model = Librarian
        fields = [
            'custom_id', 'photo', 'id_copy', 'status', 'verification_id', 'verificationid_number', 'created_date',
            'full_name', 'email', 'phone_number', 'address', 'place', 'pin_code', 'district', 'state', 'joining_date'
        ]
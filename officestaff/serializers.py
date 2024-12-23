from rest_framework import serializers
from accounts.models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields ='__all__'

class FeesHistorySerializer(serializers.ModelSerializer):
    student_fname = serializers.CharField(source='student.first_name', read_only=True)
    student_lname = serializers.CharField(source='student.last_name', read_only=True)
    class Meta:
        model = FeesHistory
        fields = ['id', 'student_fname','student_lname', 'fee_type', 'amount', 'payment_date', 'remarks', 'is_paid']
    
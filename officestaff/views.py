from django.shortcuts import render
from rest_framework import permissions,status
from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView
from accounts.models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Create your views here.
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        custom_id = request.data.get('custom_id')
        if not custom_id:
            return Response({'error': 'Custom ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(custom_id=custom_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    

class FeeHistoryListCreateView(ListCreateAPIView):
    queryset = FeesHistory.objects.all()
    serializer_class = FeesHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request,*args,**kwargs):

        if not request.user.is_superuser and not request.user.is_officestaff:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        custom_id = data.get('custom_id')
        if not custom_id:
            return Response({'error': 'Custom ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(custom_id=custom_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = FeesHistorySerializer(data=data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeeHistoryDetailView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def put(self,request,*args,**kwargs):
        fee_history_id = request.data.get('id') 
        

        if not request.user.is_superuser and not request.user.is_officestaff:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not fee_history_id:
            raise NotFound(" id not found")
        
        try:
            fees_history = FeesHistory.objects.get(id=fee_history_id)
            
        except FeesHistory.DoesNotExist:
            return Response({'error': 'Fee history not found'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = FeesHistorySerializer(fees_history, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,*args,**kwargs):
        fee_history_id = request.data.get('id')
        

        if not request.user.is_superuser and not request.user.is_officestaff:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not fee_history_id:
            return Response({"error": "Fee History ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fees_history = FeesHistory.objects.get(id=fee_history_id)
            
        except FeesHistory.DoesNotExist:
             return Response({"error": "Fee history not found"}, status=status.HTTP_404_NOT_FOUND)
            
        
        fees_history.delete()

        return Response({"message": "Fee history deleted successfully"}, status=status.HTTP_200_OK)
            

    
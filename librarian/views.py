from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from accounts.models import *
from .serializers import *

# Create your views here.


class LibraryHistoryView(APIView):
    def post(self,request,*args,**kwargs):
        custom_id = request.data.get('custom_id')
                                     
        if not custom_id:
            return Response({'error': 'Custom ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(custom_id=custom_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        data['student'] = student.id

        serializer = LibraryHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        custom_id = request.GET.get('custom_id')  # Use query parameters
        library_history_id = request.GET.get('library_history_id')

        if not request.user.is_superuser and not request.user.is_librarian:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )

    # If no data is given, return all library history
        if not custom_id and not library_history_id:
            library_history = LibraryHistory.objects.all()
            serializer = LibraryHistorySerializer(library_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # If only custom_id is provided, return all library history for that student
        if custom_id and not library_history_id:
            try:
                student = Student.objects.get(custom_id=custom_id)
            except Student.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            library_history = LibraryHistory.objects.filter(student=student)
            serializer = LibraryHistorySerializer(library_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # If both custom_id and library_history_id are provided, return specific record
        if custom_id and library_history_id:
            try:
                student = Student.objects.get(custom_id=custom_id)
            except Student.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                library_history = LibraryHistory.objects.get(id=library_history_id, student=student)
            except LibraryHistory.DoesNotExist:
                return Response({'error': 'Library History not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = LibraryHistorySerializer(library_history)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Default response if conditions are not met
        return Response({'error': 'Invalid request parameters'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request,*args,**kwargs):
        custom_id = request.data.get('custom_id')
        library_history_id = request.data.get('library_history_id')

        if not request.user.is_superuser and not request.user.is_librarian:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not custom_id or not library_history_id:
            return Response({'error': 'Custom ID and Library History ID are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(custom_id=custom_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            library_history = LibraryHistory.objects.get(id=library_history_id,student=student)
        except LibraryHistory.DoesNotExist:
            return Response({'error': 'Library History not found'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = LibraryHistorySerializer(library_history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,*args,**kwargs):
        
        library_history_id = request.data.get('library_history_id')
    

        if not request.user.is_superuser and not request.user.is_librarian:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not library_history_id:
            return Response({'error': 'Library History Id needed'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            library_history = LibraryHistory.objects.get(id=library_history_id)
        except LibraryHistory.DoesNotExist:
            return Response({'error': 'Library History not found'}, status=status.HTTP_404_NOT_FOUND)
        
            
        
        library_history.delete()
        return Response({"message": "Fee history deleted successfully"}, status=status.HTTP_200_OK)
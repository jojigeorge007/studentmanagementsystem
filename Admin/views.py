from django.shortcuts import render
from rest_framework import generics,status,permissions
from accounts.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView



        
class OfficeStaffCreateView(generics.CreateAPIView):
    serializer_class = AddOfficeStaffSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return Response({'error': 'Only admin can create office staff'}, status=status.HTTP_403_FORBIDDEN)
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'A user with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            pin_code=serializer.validated_data.get('pin_code'),
            landmark = serializer.validated_data.get('landmark'),
            district = serializer.validated_data.get('district'),
            state = serializer.validated_data.get('state'),
            country_code = serializer.validated_data.get('country_code'),
            is_officestaff=True,
            is_librarian=False,
        )

        user.set_password(password)
        user.save()

        officestaff = OfficeStaff.objects.create(
            user = user,
            photo = serializer.validated_data.get('profile_image'),
            verification_id = serializer.validated_data.get('verification_id'),
            verificationid_number = serializer.validated_data.get('verificationid_number'),
         
            status = serializer.validated_data.get('status'),  
            custom_id = None, 
        )



        officestaff.save()
        return Response({
            'message':'Office saved successfully',
            'data': serializer.data,
            'officestaff_id': officestaff.custom_id,
            'user_id': user.id,
        },status = status.HTTP_201_CREATED)


class LibrarianCreateView(generics.CreateAPIView):
    serializer_class = AddOfficeStaffSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return Response({'error': 'Only admin can create office staff'}, status=status.HTTP_403_FORBIDDEN)
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'A user with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            pin_code=serializer.validated_data.get('pin_code'),
            landmark = serializer.validated_data.get('landmark'),
            district = serializer.validated_data.get('district'),
            state = serializer.validated_data.get('state'),
            country_code = serializer.validated_data.get('country_code'),
            is_officestaff=False,
            is_librarian=True,
        )

        user.set_password(password)
        user.save()

        librarian = Librarian.objects.create(
            user = user,
            photo = serializer.validated_data.get('profile_image'),
            verification_id = serializer.validated_data.get('verification_id'),
            verificationid_number = serializer.validated_data.get('verificationid_number'),
           
            status = serializer.validated_data.get('status'),  
            custom_id = None, 
        )



        librarian.save()
        return Response({
            'message':'Librarian saved successfully',
            'data': serializer.data,
            'librarian_id': librarian.custom_id,
            'user_id': user.id,
        },status = status.HTTP_201_CREATED)
    

class OfficeStaffUpdateView(generics.UpdateAPIView):
    serializer_class = AddOfficeStaffSerializer
    
    def update(self,request,*args,**kwargs):

        if not request.user.is_superuser:
            return Response({'error': 'Only admin can update office staff'}, status=status.HTTP_403_FORBIDDEN)
            
        custom_id = request.data.get("custom_id")
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            officestaff = OfficeStaff.objects.get(custom_id=custom_id)
        except OfficeStaff.DoesNotExist:
            return Response({'error': 'Office staff not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = self.get_serializer(officestaff, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Office staff updated successfully','data':serializer.data}, status=status.HTTP_200_OK)
        



class LibrarianUpdateView(generics.UpdateAPIView):
    serializer_class = AddLibrarianSerializer
    
    def update(self,request,*args,**kwargs):


        if not request.user.is_superuser:
            return Response({'error': 'Only admin can update office staff'}, status=status.HTTP_403_FORBIDDEN)
            
        custom_id = request.data.get("custom_id")
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            librarian = Librarian.objects.get(custom_id=custom_id)
        except Librarian.DoesNotExist:
            return Response({'error': 'Librarian not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = self.get_serializer(librarian, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Librarian updated successfully','data':serializer.data}, status=status.HTTP_200_OK)
        

class OfficeStaffDeleteView(generics.DestroyAPIView):
    def delete(self,request,*args,**kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can delete office staff'}, status=status.HTTP_403_FORBIDDEN)
        
        custom_id = request.data.get("custom_id")
        
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            officestaff = OfficeStaff.objects.get(custom_id=custom_id)
        except OfficeStaff.DoesNotExist:
            return Response({'error': 'Office staff not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        officestaff.delete()
        return Response({'message':'Office staff deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class LibrarianDeleteView(generics.DestroyAPIView):
    def delete(self,request,*args,**kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can delete office staff'}, status=status.HTTP_403_FORBIDDEN)
        
        custom_id = request.data.get("custom_id")
        
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            librarian = Librarian.objects.get(custom_id=custom_id)
        except Librarian.DoesNotExist:
            return Response({'error': 'Librarian not found'}, status=status.HTTP_404_NOT_FOUND)
        

        
        librarian.delete()
        return Response({'message':'Librarian deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class OfficeStaffListView(generics.ListAPIView):
    serializer_class = OfficeStaffSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superuser can view office staff list"},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = OfficeStaff.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LibrarianListView(generics.ListAPIView):
    serializer_class = LibrarianSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superuser can view librarian list"},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = Librarian.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        custom_id = request.GET.get("custom_id",None)
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.filter(custom_id=custom_id).first()
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self,request):
        custom_id = request.data.get("custom_id",None)
        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.filter(custom_id=custom_id).first()
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        custom_id = request.data.get("custom_id",None)
        

        if not custom_id:
            return Response({'error': 'custom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.filter(custom_id=custom_id).first()
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        student.delete()
        return Response({'message':'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import LoginSerializer

class CustomLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            # Admin or staff
            if user.is_superuser or user.is_staff:
                role = "Admin"
                redirect_url = "/admin_dashboard"
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "redirect_url": redirect_url,
                    "email": user.email,
                    "full_name": user.full_name,
                }

            # Office Staff
            elif user.is_officestaff:
                role = "Office Staff"
                redirect_url = "/officestaff_dashboard"

                # Safely access related model
                office_staff = user.office_staff.first()
                if not office_staff:
                    return Response({"error": "Office staff profile not found"}, status=status.HTTP_400_BAD_REQUEST)

                custom_id = office_staff.custom_id
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "redirect_url": redirect_url,
                    "email": user.email,
                    "full_name": user.full_name,
                    "custom_id": custom_id,
                }

            # Librarian
            elif user.is_librarian:
                role = "Librarian"
                redirect_url = "/librarian_dashboard"

                # Safely access related model
                librarian = user.librarian.first()
                if not librarian:
                    return Response({"error": "Librarian profile not found"}, status=status.HTTP_400_BAD_REQUEST)

                custom_id = librarian.custom_id
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "redirect_url": redirect_url,
                    "email": user.email,
                    "full_name": user.full_name,
                    "custom_id": custom_id,
                }
            else:
                return Response({"error": "User role not defined"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

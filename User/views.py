from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer

class Users(APIView):
    """
    API view for managing user data.

    Supports GET, POST, PUT, and DELETE operations for users.
    """

    def get(self, request):
        """
        Get user(s) data based on the provided query parameters.

        If 'pk' query parameter is provided, returns data of a specific user.
        Otherwise, returns data of all users.

        Returns:
            Response: JSON response containing user data.
        """
        try:
            pk = request.query_params.get("pk")
            if pk:
                data = User.objects.get(id=pk)
                serializer = UserSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = User.objects.all()
                serializer = UserSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Requested User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Create a new user.

        Args:
            request (HttpRequest): HTTP request containing user data.

        Returns:
            Response: JSON response indicating the status of the user creation.
        """
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            email = serializer.validated_data["email"]
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            user.save()
            return Response({"message": "User Successfully created!"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Update user data.

        Args:
            request (HttpRequest): HTTP request containing updated user data.

        Returns:
            Response: JSON response indicating the status of the user update.
        """
        try:
            pk = request.query_params.get("pk")
            serializer = UserSerializer(data=request.data)
            if pk and serializer.is_valid():
                data = User.objects.get(id=int(pk))
                if data:
                    data.first_name = serializer.validated_data["first_name"]
                    data.last_name = serializer.validated_data["last_name"]
                    data.email = serializer.validated_data["email"]
                    data.save()

                    updated_serializer = serializer.data
                    return Response(updated_serializer, status=status.HTTP_200_OK)
                return Response({"message": "invalid data is provided"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Either id is wrongly put or invalid data is provided"}, status=status.HTTP_404_BAD_REQUEST)
        except:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """
        Delete a user.

        Args:
            request (HttpRequest): HTTP request containing user ID to delete.

        Returns:
            Response: JSON response indicating the status of the user deletion.
        """
        try:
            pk = request.query_params.get("pk")
            if pk:
                user = User.objects.get(id=pk)
                user.delete()
                return Response({"message": "User Successfully deleted"}, status=status.HTTP_200_OK)
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
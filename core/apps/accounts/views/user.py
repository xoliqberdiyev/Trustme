from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.accounts.serializers import user as serializers
from core.apps.accounts.models import User


class UserProfileApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=200)
    

class UserProfileUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response(serializers.UserSerializer(data).data, status=200)
        return Response(serializer.errors, status=400)
from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.contracts.models.folder import Folder
from core.apps.contracts.serializers import folder as serializers


class FolderListApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        folders = Folder.objects.filter(user=user)
        serializer = serializers.FolderListSerializer(folders, many=True)
        return Response(serializer.data, status=200)
    

class FolderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={"user": user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Folder qoshild"}, status=200)
        return Response(serializer.errors, status=400)


class FolderUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, folder_id):
        user = request.user
        folder = get_object_or_404(Folder, id=folder_id, user=user)
        serializer = self.serializer_class(data=request.data, instance=folder)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Folder tahrirlandi"}, status=200)
        return Response(serializer.errors, status=400)


class ContractListApiView(generics.GenericAPIView):
    serializer_class = serializers.FolderDetailSerializer
    queryset = Folder.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        folder = get_object_or_404(Folder, id=id, user=request.user)
        serializer = self.serializer_class(folder)
        return Response(serializer.data)
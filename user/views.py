from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .serializers import UserSerializer, TokenSerializer


# Create your views here.

class UserCreateApiView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserTokenView(APIView):
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user,
                                           data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Postman(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist("media", None)
        order = 0
        for file in files:
            order += 1
            print(order, file.name)

from rest_framework import parsers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .serializers import UserInfoSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def get_serializer_class(self):
        if self.action == "update_info":
            return UserInfoSerializer
        return super().get_serializer_class()

    @action(["GET"], False)
    def me(self, request: Request) -> Response:
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["POST"], False)
    def register(self, request: Request, permission_classes=[AllowAny]) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop("password")
        user = User(**serializer.data)
        user.set_password(password)
        user.save()

        return Response(
            self.get_serializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    @action(["PUT", "PATCH"], False, url_path="update-info")
    def update_info(self, request: Request) -> Response:
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        if password := serializer.validated_data.pop("password", None):
            request.user.set_password(password)

        serializer.save()

        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

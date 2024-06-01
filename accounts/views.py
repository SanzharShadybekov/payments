from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts import serializers
from core.tasks import send_confirmation_email_task, send_password_reset_email

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'register':
            return serializers.RegisterSerializer
        if self.action == 'activate':
            return None
        return serializers.UserSerializer

    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email_task.delay(user.email, user.activation_code)
            except Exception as e:
                print(e, '!!!!!!!!!!!!!!!!!!!!!!!!')
                return Response({'msg': 'Registered, but troubles with email!',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        try:
            user = User.objects.get(activation_code=uuid)
        except User.DoesNotExist:
            return Response({'msg': 'Invalid link or link expired!'}, status=400)

        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'Successfully activated!'}, status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


class PasswordResetViewSet(GenericViewSet):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'request_reset':
            return serializers.PasswordResetRequestSerializer
        elif self.action == 'check_reset':
            return serializers.PasswordResetCheckSerializer
        return serializers.PasswordResetSerializer

    @action(['POST'], detail=False)
    def request_reset(self, request):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        user.create_password_reset_code()
        user.save()
        send_password_reset_email.delay(user.email, user.password_reset_code)
        return Response({'msg': 'Password reset email sent.'}, status=200)

    @action(['POST'], detail=False)
    def check_reset(self, request):
        serializer = serializers.PasswordResetCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        user = User.objects.get(password_reset_code=code)
        user.password_reset_code = ''
        user.save()
        return Response({'msg': 'reset code is checked.'}, status=200)

    @action(['POST'], detail=False)
    def reset(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({'msg': 'Password has been reset.'}, status=200)

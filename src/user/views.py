from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.permissions import IsUserMineOrReadOnly
from user.serializers import SignUpSerializer, UserUpdateSerializer


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            raise exceptions.ValidationError('아이디 입력을 안했습니다.')
        if not password:
            raise exceptions.ValidationError('비밀번호 입력을 안했습니다.')

        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user_id=user.id)
            return Response(token.key)
        else:
            raise exceptions.ValidationError('비밀번호가 틀렸습니다.')


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'id'
    serializer_class = UserUpdateSerializer
    permission_classes = (
        IsUserMineOrReadOnly,
    )

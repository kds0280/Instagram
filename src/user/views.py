from cerberus.errors import BasicErrorHandler
from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from my_validator import MyValidator, check_validation
from post.base_api import CreateAPIViewWithoutSerializer
from user.models import User
from user.permissions import IsUserMineOrReadOnly
from user.serializers import SignUpSerializer, UserUpdateSerializer, UserProfileSerializer, SearchSerializer


class Login(APIView):
    def post(self, request):
        schema = {'username': {'type': 'string', 'empty': False},
                  'password': {'type': 'string', 'empty': False}}
        data = request.data.dict()
        check_validation(schema, **data)

        user = get_object_or_404(User, username=data['username'])
        if user.check_password(data['password']):
            token, created = Token.objects.get_or_create(user_id=user.id)
            return Response(token.key)
        else:
            raise exceptions.ValidationError('비밀번호가 틀렸습니다.')


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create_instance(self, request, **data_is_valid):
        instance = self.class_to_create_object.objects.create(**data_is_valid)
        instance.set_password(data_is_valid['password'])
        instance.save()
        return instance


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'id'
    serializer_class = UserUpdateSerializer
    permission_classes = (
        IsUserMineOrReadOnly,
    )

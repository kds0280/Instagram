from cerberus import Validator
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from my_validator import MyValidator


class CreateAPIViewWithoutSerializer(generics.CreateAPIView):
    schema = None
    class_to_create_object = None

    def create(self, request, *args, **kwargs):
        schema = self.schema
        validator = MyValidator(schema)
        data = request.data.dict()
        data = self.check_validation(validator, **data)
        instance = self.class_to_create_object.objects.create(**data, user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def check_validation(self, validator, **data):
        if not validator.validate(data):
            raise ValidationError
        return data

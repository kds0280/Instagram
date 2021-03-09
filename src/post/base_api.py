from cerberus import Validator
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from my_validator import MyValidator


class CreateAPIViewWithoutSerializer(generics.CreateAPIView):
    schema = None
    class_to_create_object = None

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        isvalid_data = self.check_validation(**data)
        instance = self.create_instance(request, **isvalid_data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def check_validation(self, **data):
        schema = self.schema
        validator = MyValidator(schema)
        if not validator.validate(data):
            raise ValidationError
        return data

    def create_instance(self, request, **isvalid_data):
        return self.class_to_create_object.objects.create(**isvalid_data)
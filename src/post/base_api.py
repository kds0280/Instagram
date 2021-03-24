from rest_framework import generics
from rest_framework.response import Response
from my_validator import check_validation


class CreateAPIViewWithoutSerializer(generics.CreateAPIView):
    schema = None
    class_to_create_object = None

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        data_is_valid = check_validation(self.schema, **data)
        instance = self.create_instance(request, **data_is_valid)
        serializer = self.serialize_instance(instance)
        return Response(serializer.data)

    def serialize_instance(self, instance):
        serializer = self.get_serializer(instance)
        return serializer

    def create_instance(self, request, **data_is_valid):
        return self.class_to_create_object.objects.create(**data_is_valid)

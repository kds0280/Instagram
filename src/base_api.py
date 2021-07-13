from rest_framework import generics
from rest_framework.response import Response
from my_validator import check_validation


class CreateAPIViewWithoutSerializer(generics.CreateAPIView):
    schema = None
    class_to_create_object = None

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            data = request.data
        else:
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


class UpdateAPIViewWithoutSerializer(generics.UpdateAPIView):
    def update(self, request, *args, **kwargs):
        data = request.data.dict()
        data_is_valid = check_validation(self.schema, **data)
        instance = self.get_object()
        for key, value in data_is_valid.items():
            setattr(instance, key, value)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)class RetriveAPIViewForDictionary(generics.RetrieveAPIView):
    """
    템플릿에 데이터를 전송해주기 위한 Dictionary 변환 API
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'serializer': serializer.data})


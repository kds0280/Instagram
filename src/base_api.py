from django.http import QueryDict
from rest_framework import generics
from rest_framework.response import Response
from my_validator import check_validation


class CreateAPIViewWithoutSerializer(generics.CreateAPIView):
    schema = None
    class_to_create_object = None

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            #Post의 create, User의 Create에서 QueryDict로 받는 데이터를 처리하기 위
            data = request.data.dict()
        else:
            data = request.data
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
        return Response({'serializer': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RetriveAPIViewForDictionary(generics.RetrieveAPIView):
    """
    템플릿에 데이터를 전송해주기 위한 Dictionary 변환 API
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'serializer': serializer.data})


class ListAPIViewforDictionary(generics.ListAPIView):
    """
    템플릿에 데이터를 전송해주기 위한 Dictionary 변환 API
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'serializer': serializer.data})
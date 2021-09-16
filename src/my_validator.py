import cerberus
from cerberus import Validator, errors
from cerberus.errors import BasicErrorHandler
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())


def check_validation(schema, **data):
    validator = MyValidator(schema, error_handler=BasicErrorHandler)
    if not validator.validate(data):
        for key, value in validator.errors.items():
            #어떤 field에서 오류가 발생했는지 알려주기 위함
            result = {'field': key, 'error_detail': value}
        raise ValidationError(result)
    return data


class MyValidator(Validator):
    """
    이미지 파일을 처리하기 위해 추가함
    """
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type


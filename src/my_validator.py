import cerberus
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())


def check_validation(schema, **data):
    validator = MyValidator(schema, error_handler=CustomErrorHandler)
    if not validator.validate(data):
        error_message = ''
        for key, value in validator.errors.items():
            error_message = error_message + key + ' causes an error : ' + value[0] + '   '
        raise ValidationError(error_message)
    return data


class MyValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.BAD_TYPE.code] = '은 이미지 파일이어야 합니다.'
    messages[errors.REGEX_MISMATCH.code] = '가 규격에 맞지 않습니다.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = '가 비어있습니다.'

import cerberus
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())


def check_validation(schema, **data):
    validator = MyValidator(schema, error_handler=BasicErrorHandler)
    if not validator.validate(data):
        error_message = ''
        for key, value in validator.errors.items():
            error_message = error_message + key + ' causes an error : ' + value[0] + '   '
        raise ValidationError(error_message)
    return data


class MyValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type


import cerberus
from cerberus import Validator, errors
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())


def check_validation(schema, **data):
    if not validator.validate(data):
        for key, value in validator.errors.items():
        raise ValidationError(result)
    return data


class MyValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type


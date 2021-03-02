import cerberus
from cerberus import Validator
from django.core.files.uploadedfile import InMemoryUploadedFile

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())


class MyValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type

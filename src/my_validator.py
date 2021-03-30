import cerberus
from cerberus import Validator, errors
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

file_type = cerberus.TypeDefinition('file', (InMemoryUploadedFile,), ())
error_field_list = {
    'username': "아이디",
    'password': "비밀번호",
    'phone_number': "전화번호",
    'email': "이메일",
    'description': "프로필 본문",
    'profile_image': "프로필 사진",
    'post_body': "글 본문",
    'post_image': "포스트 사진",
    'post_id': "포스트",
    'parent_id': "상위 댓글",
    'comment_body': "댓글 본문",
}


def check_validation(schema, **data):
    validator = MyValidator(schema, error_handler=CustomErrorHandler)
    if not validator.validate(data):
        error_message = ''
        for key, value in validator.errors.items():
            error_field = error_field_list[key]
            error_message = error_message + error_field + value[0]
            result = {'error': error_message}
        raise ValidationError(result)
    return data


class MyValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file'] = file_type


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.BAD_TYPE.code] = '은 이미지 파일이어야 합니다.'
    messages[errors.REGEX_MISMATCH.code] = '가 규격에 맞지 않습니다.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = '가 비어있습니다.'

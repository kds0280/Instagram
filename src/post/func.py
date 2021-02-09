from post.models import Post


def post_create(user, body):
    """
    - user 는 arguments 로 받기
    - 그 외 데이터 arguments 로 받기
    """
    return Post.objects.create(user=user, body=body)


def post_list():
    """
    - 모든 포스트를 리스트로 반환하기
    - 각 포스트는 아래의 정보를 담은 딕셔너리로 변환
        - username, email, description, phone_number
    """
    post_list = []
    for i in Post.objects.prefetch_related('user'):
        post_data = {'username': i.user.username, 'email': i.user.email, 'description': i.user.description,
                     'phone_number': i.user.phone_number}
        post_list.append(post_data)
    return post_list


def post_detail(post_id):
    """
    - 가장 적은 argument 를 받기
    - 아래 데이터를 딕셔너리로 반환
        - username, email, description, phone_number, 좋아요한 포스트 수
    """
    post = Post.objects.get(pk=post_id)
    return {
        'username': post.user.username,
        'email': post.user.email,
        'description': post.user.description,
        'phone_number': post.user.phone_number,
        '좋아요한 포스트 수': post.like_count,
    }


def post_update(post_id, body):
    """
    - user 는 변경 금지
    - 그 외 데이터 arguments로 받기
    """
    post = Post.objects.get(pk=post_id)
    post.body = body
    post.save()


def post_delete(post_id):
    """
    - 가장 적은 argument 를 받아서 삭제하기
    """
    post = Post.objects.get(pk=post_id)
    post.delete()

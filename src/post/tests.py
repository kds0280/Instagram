from rest_framework.test import APITestCase

from post.models import Post
from user.models import User


class UserModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="hayoung", password='1234',
                            phone_number="010-5835-0925")

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_username_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 150)

    def test_phone_number_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label,'phone number')

    def test_phone_number_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 13)

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_username_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_description_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_like_posts_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('like_posts').verbose_name
        self.assertEqual(field_label, 'like posts')

    def test_like_posts_relate(self):
        user = User.objects.get(id=1)
        post = user.like_posts.create(user=user)
        self.assertEqual(user.like_posts.get(id=post.id), post)

    def test_like_posts_related_name(self):
        user = User.objects.get(id=1)
        post = user.like_posts.create(user=user)
        self.assertEqual(user.like_posts.get(id=post.id), post)

    def test_like_followings_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('followings').verbose_name
        self.assertEqual(field_label, 'followings')

    def test_profile_image_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('profile_image').verbose_name
        self.assertEqual(field_label, 'profile image')

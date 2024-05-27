
from django.contrib.auth import get_user
from .models import CustomUser
from django.test import TestCase
from django.urls import reverse


class TestRegistration(TestCase):
    def  test_user_registration(self):
        self.client.post(
            reverse('users:register'),

            data={
                'username':'ali',
                'first_name': 'aliyev',
                'last_name': 'valiyev',
                'email':'ali008@gmail.com',
                'password':'password1'
            }

        )
        user = CustomUser.objects.get(username= 'ali')

        self.assertEqual(user.first_name, 'aliyev')
        self.assertEqual(user.last_name, 'valiyev')
        self.assertEqual(user.email, 'ali008@gmail.com')
        self.assertNotEquals(user.password, 'password1')
        self.assertTrue(user.check_password('password1'))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'first_name': 'aliyev',
                'password': '<PASSWORD>',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response,'form', 'username', 'This field is required.')
        self.assertFormError(response, "form", "password", "This field is required.")

    def  test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),

            data={
                'username':'ali',
                'first_name': 'aliyev',
                'las_name': 'valiyev',
                'email':'34@gmai',
                'password':'password1'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_invalid_password(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'ali',
                'first_name': 'aliyev',
                'last_name': 'valiyev',
                'email': 'ali008@gmail.com',
                'password': '$$$^&&*&%%$$%'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'password', 'Enter a valid password.')

class LoginTest(TestCase):
    def test_success_login(self):
        db_user =  CustomUser.objects.create(username = 'ali', first_name = 'aliyev')
        db_user.set_password('password1')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'ali',
                'password': 'password1'
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)


    def test_wrong_login(self):
        db_user = CustomUser.objects.create(username='ali', first_name='aliyev')
        db_user.set_password('password1')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'other-user',
                'password': 'password1'
            }
        )
        user = get_user(self.client)


        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('login'),
            data={
                'username': 'ali',
                'password': 'wrong-password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="ali", password="password1")
        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + '?next=/users/profile/')

    def test_profile_detail(self):
        user = CustomUser.objects.create(username="ali",
                                    first_name="aliyev",
                                    last_name="valiyev",
                                    email="ali008@gmail.com")

        user.set_password("<PASSWORD>")
        user.save()

        self.client.login(username="ali", password="<PASSWORD>")
        response = self.client.get(reverse("users:profile"))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UserRegisterTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.anonymous_client = APIClient()
        self.user_info = {"email": "user@gmail.com", "password": "pwd"}

    def test_register_user(self):
        response = self.anonymous_client.post(
            reverse("users:users-register"),
            self.user_info,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {"id": 1, "username": "user", "email": "user@gmail.com", "image": None},
        )


class UserTestCase(APITestCase):
    user_info = {"email": "user@gmail.com", "password": "pwd"}

    def setUp(self) -> None:
        super().setUp()
        self.anonymous_client = APIClient()
        # jwt login user
        self.user = self.client.post(reverse("users:users-register"), self.user_info)
        self.access_token = self.get_user_token(data=self.user_info).data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def get_user_token(self, data):
        return self.client.post(reverse("token_obtain_pair"), data)

    def get_me(self, client=None):
        client = client or self.client
        return client.get(reverse("users:users-me"))

    def test_get_user_info(self):
        response = self.get_me()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 1, "username": "user", "email": "user@gmail.com", "image": None},
        )

    def test_anonymous_get_user_info_is_fail(self):
        response = self.get_me(client=self.anonymous_client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def update_info(self, client=None):
        client = client or self.client
        return client.patch(
            reverse("users:users-update-info"),
            {"password": "changepwd"},
        )

    def test_update_info(self):
        self.update_info()
        before_response = self.get_user_token(data=self.user_info)
        after_response = self.get_user_token(
            data={"email": "user@gmail.com", "password": "changepwd"},
        )
        self.assertEqual(before_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(after_response.status_code, status.HTTP_200_OK)

    def test_anonymous_update_info_is_fail(self):
        response = self.update_info(client=self.anonymous_client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

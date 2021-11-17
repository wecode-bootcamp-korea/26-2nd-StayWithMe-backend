import jwt, os, json

from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase
from django.conf   import settings
from staywithme.settings import ALGORITHM

from users.models  import User

class UserLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            id        = 1,
            email     = 'lck0827@gmail.com',
            kakao_id  = 123456789,
            nick_name = 'chankyu'
        )

    def tearDown(self) :
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_signin_post_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 123456781, 
                    'kakao_account': 
                        {
                            'email'   : 'lck08271@gmail.com',
                            'profile' : {
                                "nickname" : "chankyuu"
                            }
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'nhPutu-CpoH9dRCboKNmdAznw6i6zbLwwWM'}
        response            = client.post('/users/signin', **headers)
        access_token        = jwt.encode({'id': 2}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'access_token': access_token
        })

    @patch('users.views.requests')
    def test_kakao_signin_post_existing_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 123456789, 
                    'kakao_account': 
                        {
                            'email'   : 'lck0827@gmail.com',
                            'profile' : {
                                "nickname" : "chankyu"
                            }
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'nhPutu-CpoH9dRCboKNmdAznw6i6zbLwwWM'}
        response            = client.post('/users/signin', **headers)
        access_token        = jwt.encode({'id': 1}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'access_token': access_token
        })

    @patch('users.views.requests')
    def test_kakao_signin_post_invalid_token(self, mocked_requests):
        client   = Client()
        headers  = {}
        response = client.post('/users/signin', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})
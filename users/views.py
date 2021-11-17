import json, jwt, requests, os

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from .models      import User

class KakaoSignInView(View):
    def post(self, request):
        try:
            access_token = request.headers['Authorization']
            response     = requests.get('https://kapi.kakao.com/v2/user/me', headers=({'Authorization': f'Bearer {access_token}'})).json()

            kakao_id     = response['id']
            email        = response['kakao_account']['email']
            nickname     = response['kakao_account']['profile']['nickname']

            user, created = User.objects.get_or_create(
                kakao_id  = kakao_id, 
                email     = email, 
                nick_name = nickname
            )

            http_status_code = 201 if created else 200
            token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)            

            return JsonResponse({'message': 'SUCCESS', 'access_token' : token}, status = http_status_code)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

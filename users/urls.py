from django.urls import path
from users.views import KakaoSignInView

urlpatterns=[
    path("/signin", KakaoSignInView.as_view()),
]

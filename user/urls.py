from django.urls import path

from .views import UserCreateApiView, UserTokenView, \
    UserRetrieveUpdateApiView, Postman

app_name = "user"

urlpatterns = [
    path('create/', UserCreateApiView.as_view(), name="create"),
    path('token/', UserTokenView.as_view(), name="token"),
    path('me/', UserRetrieveUpdateApiView.as_view(), name="me"),
    path('postman/', Postman.as_view(), name="postman")
]

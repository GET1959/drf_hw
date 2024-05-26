from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(permission_classes=(AllowAny,)), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("", UserListAPIView.as_view(), name="user_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
urlpatterns += router.urls

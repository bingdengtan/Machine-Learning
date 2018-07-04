from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserBaseViewSet

router = DefaultRouter()
router.register(r'user', UserBaseViewSet, base_name='user')

urlpatterns = [
    url(r'^', include(router.urls)),  # Api Root
    url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
]
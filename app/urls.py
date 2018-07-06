from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserBaseViewSet, JSONWebTokenObtainViewSet

router = DefaultRouter()
router.register(r'user', UserBaseViewSet, base_name='user')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth-jwt/', JSONWebTokenObtainViewSet.as_view()),
]

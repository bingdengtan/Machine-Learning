from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import UserBaseViewSet, RoleBaseViewSet, ProjectProfileViewSet, ModelProfileViewSet
from .views import JSONWebTokenObtainViewSet, MLViewSet

router = DefaultRouter()
router.register(r'adm/user', UserBaseViewSet, base_name='user')
router.register(r'adm/role', RoleBaseViewSet, base_name='role')
router.register(r'adm/project', ProjectProfileViewSet, base_name='project_profile')
router.register(r'adm/model', ModelProfileViewSet, base_name='model_profile')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth-jwt/', JSONWebTokenObtainViewSet.as_view()),
    url(r'ml/', MLViewSet.as_view()),
]
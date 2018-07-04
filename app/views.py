from rest_framework import viewsets, permissions, renderers
from django.shortcuts import get_object_or_404

from .serializers import UserBaseSerializer
from .models import User_Base
from .permissions import IsAuthenticated

# Create your views here.


class UserBaseViewSet(viewsets.ModelViewSet):
    queryset = User_Base.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

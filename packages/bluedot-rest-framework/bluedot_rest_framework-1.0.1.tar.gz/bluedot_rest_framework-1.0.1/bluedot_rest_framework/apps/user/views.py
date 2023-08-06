from rest_framework.response import Response
from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from .models import User
from .serializers import UserSerializer
from .frontend_views import FrontendView


class UserView(CustomModelViewSet, FrontendView):
    model_class = User
    serializer_class = UserSerializer

    filterset_fields = {
        '_exists': '',
        'wechat_profile__nick_name': {
            'type': 'string',
            'filter': '__contains'
        },
    }

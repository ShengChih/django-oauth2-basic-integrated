from rest_framework import status, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.response import Response

from social_auth.serializers import (
    PROVIDER_SERIALIERS
)
from libs.jwt.functools import get_tokens_for_user

import traceback
import logging


logger = logging.getLogger(__name__)


@api_view(['POST'])
def exchange_token(request):
    try:
        provider_name = request.data.get('provider_name')
        serializer_class = PROVIDER_SERIALIERS.get(provider_name)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get_user_model()
        tokens = get_tokens_for_user(user)
    except Exception:
        logger.error(traceback.format_exc())
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(data=tokens)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    return Response({"message": "OK"})

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(exclude=True)
class HealthView(APIView):
    permission_classes = (AllowAny, )

    def get(self, *args, **kwargs):
        data = {'status': 'ok'}
        return Response(data)

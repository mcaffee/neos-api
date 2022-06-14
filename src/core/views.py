from typing import Type, Any

from django.http import Http404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import DoesNotExist

HandlerSerializer = Type[serializers.Serializer]


class GenericHandlerAPIView(APIView):
    request_serializer_class: HandlerSerializer = None
    response_serializer_class: HandlerSerializer = None
    result_to_dict = False

    def handler(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def run_handler(self) -> Any:
        try:
            handler_kwargs = self.get_handler_kwargs()
            handler_result = self.handler(**handler_kwargs)

            data = self.process_handler_result(result=handler_result)
            result = self.prepare_response_data(data=data)
        except DoesNotExist:
            raise Http404

        return result

    def get_handler_kwargs(self) -> dict:
        return {}

    def process_handler_result(self, result) -> Any:
        if self.result_to_dict:
            method_exists = (hasattr(result, 'dict') and callable(result.dict))
            if method_exists:
                result = result.dict()

        return result

    def get_request_serializer_data(self) -> dict:
        assert self.request_serializer_class is not None, (
            "'%s' should include a `request_serializer_class` attribute."
            % self.__class__.__name__
        )

        request_serializer = self.request_serializer_class(
            data=self.request.data,
        )
        request_serializer.is_valid(raise_exception=True)

        return request_serializer.validated_data

    def prepare_response_data(self, data):
        if not self.response_serializer_class:
            return data

        response_serializer = self.response_serializer_class(instance=data)
        return response_serializer.data


class GetHandlerAPIView(GenericHandlerAPIView):
    def get(self, *args, **kwargs):
        result = self.run_handler()
        return Response(result, status=status.HTTP_200_OK)


class PostHandlerAPIView(GenericHandlerAPIView):
    def post(self, *args, **kwargs):
        result = self.run_handler()
        return Response(result, status=status.HTTP_200_OK)

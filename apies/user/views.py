from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloApi(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={"message": "hello word"}, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework.views import APIView

from .data import pets
from .serializers import PetPolymorphicSerializer


class PetView(APIView):
    serializer_class = PetPolymorphicSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(pets, many=True)
        return Response(serializer.data)


from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class AuthorViewSet(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated,]
    serializer_class = AuthorSerializer


    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)

        return qs

    @action(
            detail=False,
            methods=['get'],
        )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)

        return Response(serializer.data)
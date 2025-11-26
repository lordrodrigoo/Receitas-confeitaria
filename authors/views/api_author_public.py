# authors/views/api_author_public.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


User = get_user_model()

class ProfileDetailAPIv1View(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'detail': 'Não encontrado.'}, status=404)
        
        profile = getattr(user, 'profile', None)
        bio = getattr(profile, 'bio', '') if profile else ''
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': bio,
        })
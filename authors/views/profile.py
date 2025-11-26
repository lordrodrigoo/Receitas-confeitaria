from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from authors.models import Profile




class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('id')
        profile = get_object_or_404(Profile.objects.select_related('author'), pk=profile_id)
        context = self.get_context_data(**kwargs)
        context['profile'] = profile
        return self.render_to_response(context)
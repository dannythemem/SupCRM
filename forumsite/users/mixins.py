from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from posts.models import Posts, Like


class UsersPostsFilterMixin(ListView):
    reaction_type = None
    empty_list_text = None
    template_name = 'users/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(get_user_model(), username=username)

        if self.reaction_type is None:
            return Posts.objects.filter(author=user)
        return Posts.objects.filter(
            posts_likes__user=user,
            posts_likes__reaction_type=self.reaction_type
        ).with_reactions()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['viewed_user'] = get_object_or_404(get_user_model(), username=username)
        context['title'] = get_object_or_404(get_user_model(), username=username).username
        context['empty_list_text'] = self.empty_list_text
        return context
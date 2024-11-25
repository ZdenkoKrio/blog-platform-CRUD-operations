from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import CustomUserCreationForm
from posts.models import Post


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['bio', 'profile_picture', 'website', 'twitter', 'facebook', 'instagram']
    template_name = 'users/profile_form.html'

    def get_object(self, queryset=None):
         return get_object_or_404(UserProfile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user-profile', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        return self.get_object().user == self.request.user


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            return post.author

        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object).order_by('-created_at')
        return context

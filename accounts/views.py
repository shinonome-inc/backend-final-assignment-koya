from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import Friendship, User
from tweets.models import Like, Tweet

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/profile.html"
    context_object_name = "tweets"

    def get_queryset(self):
        username = self.kwargs.get("username")
        self.profile_user = get_object_or_404(User, username=username)
        queryset = (
            Tweet.objects.filter(user=self.profile_user)
            .select_related("user")
            .annotate(total_likes=Count("like_tweet"))
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user
        user_following_friendships = list(
            Friendship.objects.filter(follower=self.request.user).select_related("following")
        )
        user_following = [friendship.following for friendship in user_following_friendships]
        following_number = Friendship.objects.filter(follower=self.profile_user).count()
        follower_number = Friendship.objects.filter(following=self.profile_user).count()
        user_likes = set(Like.objects.filter(likeuser=self.request.user).values_list("liketweet_id", flat=True))
        context["user_following"] = user_following
        context["following_number"] = following_number
        context["follower_number"] = follower_number
        for tweet in context["tweets"]:
            tweet.liked_by_user = tweet.id in user_likes

        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        following_user = get_object_or_404(User, username=username)
        is_following = Friendship.objects.filter(follower=request.user, following=following_user).exists()
        if request.user == following_user:
            return HttpResponseBadRequest("自分自身をフォローすることはできません")
        elif is_following:
            return HttpResponseBadRequest("すでにフォローしています")
        else:
            follow_instance = Friendship(follower=request.user, following=following_user)
            follow_instance.save()
            return HttpResponseRedirect(reverse_lazy("tweets:home"))


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        unfollowing_user = get_object_or_404(User, username=username)
        follow_instance = Friendship.objects.filter(follower=request.user, following=unfollowing_user)
        if request.user == unfollowing_user:
            return HttpResponseRedirect("自分自身をアンフォローすることはできません")
        elif not follow_instance:
            return HttpResponseBadRequest("すでにアンフォロー中です")
        else:
            follow_instance.delete()
            return HttpResponseRedirect(reverse_lazy("tweets:home"))


class FollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/following_list.html"
    context_object_name = "following_list"

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Friendship.objects.all().filter(follower=self.user).select_related("following").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    template_name = "accounts/follower_list.html"
    context_object_name = "follower_list"

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Friendship.objects.all().filter(following=self.user).select_related("follower").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context

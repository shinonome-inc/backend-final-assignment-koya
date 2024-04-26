from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from tweets.forms import CreateTweetForm

from .models import Tweet

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator



class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    context_object_name = "tweets"

    def get_queryset(self):
        return Tweet.objects.select_related("user").order_by("created_at")


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    model = Tweet
    form_class = CreateTweetForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = Tweet


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = Tweet
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


# class LikeView(LoginRequiredMixin, View):
#     templete_nane = "tweets/home.html"

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, pk):
#         tweet = Tweet.objects.get(pk=pk)
#         tweet.likes.add(request.user)
#         return JsonResponse({"status": "ok"})


# class UnlikeView(LoginRequiredMixin, View):
#     templete_nane = "tweets/home.html"

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, pk):
#         tweet = Tweet.objects.get(pk=pk)
#         tweet.likes.remove(request.user)
#         return JsonResponse({"status": "ok"})

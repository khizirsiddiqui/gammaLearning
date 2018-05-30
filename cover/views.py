from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Board, Topic, Post, SchoolProfile
from .forms import NewTopicForm, PostForm

from notification.models import Notification

from scripts.quotes import img_quotes
from scripts.words import rand_word
from scripts.news import get_news


def homePage(request):
    boards = Board.objects.all()
    quote = img_quotes()
    word = rand_word()
    ## news = get_news()
    news = None
    return render(request, 'index.html', {'boards': boards, 'quote': quote, 'word': word, 'news': news, })


class TopicListView(ListView):
    model = Topic
    paginate_by = 15
    context_object_name = 'topics'
    template_name = 'topics.html'

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by(
            '-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics, })


def school_profile(request, pk):
    school = get_object_or_404(SchoolProfile, pk=pk)
    student_list = school.get_student_list()
    return render(request, 'school_profile.html', {'school': school, 'student_list': student_list, })


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get(
            'pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            messages.add_message(request, messages.SUCCESS, 'New Topic Opened')

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={
                                'pk': pk, 'topic_pk': topic_pk})

            if post.created_by.username != topic.starter.username:
                topic_notif = post.created_by.username + ' replied to ' + topic.subject
                notif = Notification(
                    user=topic.starter, message=topic_notif, level=2, link=topic_url, fa_type='fa-edit')
                notif.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Reply to the topic successfull.')

            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    success_message = "Post successfully updated."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@login_required
def post_upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user.is_authenticated:
        dec = post.upvote(user)
        if dec == 1:
            topic_notif = user.username + ' Upvoted your post in ' + post.topic.subject
            topic_url = reverse('topic_posts', kwargs={
                                'pk': post.topic.board.pk, 'topic_pk': post.topic.pk})
            notif = Notification(
                    user=post.created_by, message=topic_notif, level=2, link=topic_url, fa_type='fa-seedling')
            notif.save()
            messages.add_message(
                request, messages.SUCCESS, 'Post Upvoted')
        elif dec == 2:
            messages.add_message(
                request, messages.INFO, 'Post Already Voted')
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
    else:
        messages.add_message(
            request, messages.ERROR, 'Please login/register to Upvote')
        return redirect('login')


@login_required
def post_downvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user.is_authenticated:
        dec = post.downvote(user)
        if dec == 1:
            messages.add_message(
                request, messages.SUCCESS, 'Post DownVoted')
        elif dec == 2:
            messages.add_message(
                request, messages.INFO, 'Post already Voted')
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
    else:
        messages.add_message(
            request, messages.ERROR, 'Please login/register to Vote')
        return redirect('login')

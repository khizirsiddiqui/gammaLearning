from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings as django_settings
from django.dispatch import receiver

# Create your models here.


def school_image_path(instance, filename):
    return 'images/schools/{0}_{1}'.format(instance.name, filename)


class SchoolProfile(models.Model):
    name = models.TextField(blank=False)
    points = models.PositiveIntegerField(default=0)
    website = models.URLField(default='', blank=True)
    image = models.ImageField(upload_to=school_image_path, blank=True)
    address = models.TextField(blank=True)
    country = models.TextField(blank=False, default='IN')

    def __str__(self):
        self.points_update()
        return self.name

    def points_update(self):
        points = 0
        for student in StudentProfile.objects.filter(school=self):
            points += student.reputation
        self.points = points
        self.save()
        return True

    def get_student_count(self):
        student_list = StudentProfile.objects.filter(school=self)
        return student_list.count()

    def get_student_list(self):
        return StudentProfile.objects.filter(school=self)


class StudentProfile(models.Model):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete='cascade')
    name = models.CharField(max_length=20, blank=True, default='')
    bio = models.TextField(default='', blank=True)
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    school = models.ForeignKey(
        SchoolProfile, on_delete=models.CASCADE, related_name='school')
    reputation = models.PositiveIntegerField(default=0)

    def rep_update(self):
        a = self.get_post_count()
        b = self.get_topic_count()
        c = 0
        d = 0
        e = 0
        f = 0
        for post in Post.objects.filter(created_by=self.user):
            c += post.upvotes
            d += post.downvotes
        for topic in Topic.objects.filter(starter=self.user):
            e += topic.upvotes
            f += post.downvotes

        rep = (a + b) * 1.5 + (c) * 2 - d + e * 2.5 - f * 3
        self.reputation = rep
        self.save()
        return True

    def get_post_count(self):
        return Post.objects.filter(created_by=self.user).count()

    def get_topic_count(self):
        return Topic.objects.filter(starter=self.user).count()

    def get_recent_posts(self):
        return Post.objects.filter(created_by=self.user).order_by('-created_at')

    def get_name(self):
        self.rep_update()
        return self.user.first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = StudentProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(
        Board, related_name='topics', on_delete=models.CASCADE,)
    starter = models.ForeignKey(
        User, related_name='topics', on_delete=models.CASCADE,)
    views = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(User, related_name='voters', blank=True)

    def __str__(self):
        return self.subject

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


def post_image_path(instance, filename):
    return 'images/topic_{0}/{1}'.format(instance.topic.pk, filename)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        Topic, related_name='posts', on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE,)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.CASCADE,)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(
        User, related_name='post_voters', blank=True)
    image = models.ImageField(
        upload_to=post_image_path, default='', blank=True)

    def get_last_datetime(self):
        if self.updated_at is None:
            return self.created_at
        else:
            return self.updated_at

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def upvote(self, voter):
        if voter not in self.voters.all():
            self.upvotes += 1
            self.voters.add(voter)
            self.save()
            return 1
        else:
            return 2
        return 0

    def downvote(self, voter):
        if voter not in self.voters.all():
            self.downvotes += 1
            self.voters.add(voter)
            self.save()
            return 1
        else:
            return 2
        return 0

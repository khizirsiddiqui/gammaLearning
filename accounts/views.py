from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.views.generic import ListView

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from cover.models import StudentProfile, SchoolProfile, Topic
from .forms import SignUpForm, UserForm

# Create your views here.


@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(
        User, StudentProfile, fields=('bio', 'gender', 'school'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(
                request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(
                    request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    messages.add_message(
                        request, messages.SUCCESS, 'Yay! Profile Updated')
                    return redirect('home')
        return render(request, 'my_account.html', {'form': user_form, 'formset': formset})
    else:
        raise PermissionDenied


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Hello' +
                                 user.username + '. Try Completing your profile. :)')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, })


def school_profile(request, pk):
    school = get_object_or_404(SchoolProfile, pk=pk)
    student_list = school.get_student_list()
    return render(request, 'school_profile.html', {'school': school, 'student_list': student_list, })


def student_profile(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    recent_posts = student.get_recent_posts()
    all_topics = Topic.objects.filter(starter=student.user)
    return render(request, 'student_profile.html', {'student': student, 'recent_posts': recent_posts,
                                                    'all_topics': all_topics})


class schoolListView(ListView):
    queryset = SchoolProfile.objects.all().order_by('-points')
    context_object_name = 'schools'
    template_name = 'school_list.html'

    def get_object(self):
        object = super.get_object()
        object.points_update()
        return object


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Username already Occupied. Try a New One'
    else:
        data['success_message'] = 'Username available.'
    return JsonResponse(data)


def get_user_popup(request):
    username = request.GET.get('username', None)
    target = get_object_or_404(User, username=username)
    profile = get_object_or_404(StudentProfile, user=target)
    json_obj = model_to_dict(profile)
    return JsonResponse(json_obj)

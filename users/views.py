from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import *
from .models import ProfileModel
from django.contrib.auth.models import User
from django.db.models import Q
import os
# Create your views here.

def image_get(request, pk_username):
    if request.method == 'GET':
        if ProfileModel.objects.filter(pk=pk_username).exists():
            return JsonResponse({'img': ProfileModel.objects.get(pk=pk_username).image.url})
        else:
            return JsonResponse({'img': ''})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users-login')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'users/sign_up.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilemodel)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': PostModel.objects.filter(author=request.user),
    }
    return render(request, 'users/profile.html', context)
@login_required
def profile_pk(request, pk_username):
    u_form = UserUpdateForm(instance=User.objects.get(pk=pk_username))
    p_form = ProfileUpdateForm(instance=User.objects.get(pk=pk_username).profilemodel)
    user = User.objects.get(pk=pk_username)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'posts': PostModel.objects.filter(author=user),
    }
    return render(request, 'users/profile_pk.html', context)

@login_required
def send_message_on_profile(request, pk_username):
    if request.method == 'POST':
        message = Messages()
        message.author = request.user
        message.user_output = User.objects.get(pk=pk_username)
        message.message = request.POST.get('message')
        message.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def chat(request, pk_username):
    if request.method == 'POST':
        message = Messages()
        message.author = request.user
        message.user_output = User.objects.get(pk=pk_username)
        if request.POST.get('message') == '':
            return redirect(request.META.get('HTTP_REFERER'))
        message.message = request.POST.get('message')
        message.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        user_output = User.objects.get(pk=pk_username)
        messages_author = Messages.objects.filter(Q(author=request.user) & Q(user_output=user_output))
        messages_user = Messages.objects.filter(Q(author=user_output) & Q(user_output=request.user))
    context = {
        'chat': messages_author.union(messages_user).order_by("date_created"),
    }
    return render(request, 'blog/post_chat.html', context)

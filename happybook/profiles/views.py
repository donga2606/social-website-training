from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .form import ProfileModelForm
from django.views.generic import ListView, DetailView
# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    invites = Relationship.objects.invitation_received(profile)
    results = list(map(lambda x: x.sender, invites))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {'invites': results, 'is_empty': is_empty}
    return render(request, 'profiles/my_invites.html', context)

@login_required
def accepted_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('sender_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my_invites')

@login_required
def rejected_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('sender_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my_invites')




# def profiles_list_view(request):
#     # This is all profile except the user is requesting
#     user = request.user
#     profiles = Profile.objects.get_all_profiles(user)
#
#     context = {
#         'profiles': profiles,
#     }
#     return render(request, 'profiles/profiles_list.html', context)

# @login_required
def invite_profiles_list_view(request):
    # This is all profile except the user is requesting
    user = request.user
    profiles = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'profiles': profiles,
    }
    return render(request, 'profiles/invite_profiles_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile
    def get_context_data(self, **kwargs):
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = [i.receiver.user for i in rel_r]
        rel_sender = [i.sender.user for i in rel_s]
        kwargs['rel_receiver'] = rel_receiver
        kwargs['rel_sender'] = rel_sender
        kwargs['posts'] = self.get_object().get_all_author_posts()
        kwargs['len_posts'] = True if len(self.get_object().get_all_author_posts()) > 0 else False
        return super().get_context_data(**kwargs)


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'profiles'
    def get_queryset(self):
        user = self.request.user
        profiles = Profile.objects.get_all_profiles(user)
        return profiles

    def get_context_data(self, **kwargs):
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = [i.receiver.user for i in rel_r]
        rel_sender = [i.sender.user for i in rel_s]
        kwargs['rel_receiver'] = rel_receiver
        kwargs['rel_sender'] = rel_sender
        kwargs['is_empty'] = False
        if len(self.get_queryset()) == 0:
            kwargs['is_empty'] = True
        return super().get_context_data(**kwargs)

@login_required()
def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile')

@login_required()
def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile')

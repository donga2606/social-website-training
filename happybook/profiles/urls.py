from .views import (
    my_profile_view,
    invites_received_view,
    ProfileDetailView,
    ProfileListView,
    invite_profiles_list_view,
    send_invitation,
    remove_from_friends,
    accepted_invitation,
    rejected_invitation,
)
from django.urls import path

app_name = 'profiles'
urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles'),
    path('myprofile/', my_profile_view, name='my_profile'),
    path('invites/', invites_received_view, name='my_invites'),
    path('to_invites/', invite_profiles_list_view, name='all_invite_profiles'),
    path('send_invite/', send_invitation, name='send_invite'),
    path('remove-friend/', remove_from_friends, name='remove_friend'),
    path('invites/accept/', accepted_invitation, name='accept_invite'),
    path('invites/reject', rejected_invitation, name='reject_invite'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile_detail'),
]

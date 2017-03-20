from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.utils import timezone
from django.contrib.auth.models import User
from manual_facebook.models import FacebookStatus
import facebook
from forms import FacebookStatusForm

@login_required
def home(request):
    forms = FacebookStatusForm()
    return render(request, 'home.html', {'forms':forms})

def about(request):
    return render(request, "about.html")

@login_required
def settings(request):
        user = request.user
        try:
            facebook_login = user.social_auth.get(provider='facebook')

        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        return render(request, 'settings.html', {
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        })

def update_facebook(request):
    # import ipdb; ipdb.set_trace()
    user = User.objects.get(id=request.user.id)
    forms = FacebookStatusForm(request.POST)
    if forms.is_valid():
        messages = forms.cleaned_data['message']
        status = FacebookStatus.objects.create(author=user,
                                                 status='approved',
                                                 publish_timestamp=timezone.now(),
                                                 message=messages,
                                                 link=None)
        auth = user.social_auth.first()
        graph = facebook.GraphAPI(auth.extra_data['access_token'])
        try:

            graph.put_object('me', 'feed', message=messages)
            status.publish_timestamp = timezone.now()
            status.save()
        except Exception as ex:
            print ex
            link = "https://developers.facebook.com/tools/explorer/1270412293034840?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.8 "
            return render(request, 'home.html', {'forms': forms, 'link': link})
        forms = FacebookStatusForm()
    return render(request, 'home.html', {'forms': forms})

@login_required
def password(request):
        if request.user.has_usable_password():
            PasswordForm = PasswordChangeForm
        else:
            PasswordForm = AdminPasswordChangeForm

        if request.method == 'POST':
            form = PasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordForm(request.user)
        return render(request, 'password.html', {'form': form})

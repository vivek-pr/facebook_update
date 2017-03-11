from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.utils import timezone
from django.contrib.auth.models import User
from manual_facebook.models import FacebookStatus
import facebook
from django.http import HttpResponse
from forms import FacebookStatusForm

@login_required
def home(request):
    forms = FacebookStatusForm()
    return render(request, 'home.html', {'forms':forms})

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
        graph.put_object('me', 'feed', message=messages)
        status.publish_timestamp = timezone.now()
        status.save()
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
# def login_page(request):
#     return render(request, "login.html",{})


# def acquire_facebook_oauth_code():
#     redirect_uri = 'http://localhost:8000/'
#     attrs = {'client_id': settings.FACEBOOK_APP_ID,
#              'redirect_uri': redirect_uri,
#              'scope':'offline_access,publish_stream,manage_pages'}
#     code_url = 'https://graph.facebook.com/oauth/authorize?%s'  % urllib.urlencode(attrs)
#     print code_url
#     return code_url
#
#
# def handle_facebook_redirect(request):
#     code = request.GET.get('code')
#
#     attrs = {'client_id': settings.FACEBOOK_APP_ID,
#              'client_secret': settings.FACEBOOK_APP_SECRET,
#              'code': code}
#     access_token_url = 'https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(attrs)
#
#     r = requests.get(access_token_url)
#     access_token = urlparse.parse_qs(r.content)['access_token'][0]
#
#     # save the access_token for your user
#     user_profile = request.user.get_profile()
#     user_profile.facebook_access_token = access_token
#     user_profile.save()
#
#     return redirect('facebook_succeeded_page')
#
#
# @login_required
# def share_on_facebook(request):
#     payload = dict(message= & quot;
#     Your
#     fancy
#     facebook
#     wall
#     status & quot;),
#     access_token = request.user.get_profile().facebook_access_token)
#
#     req = requests.post('https://graph.facebook.com/feed', data=payload)
#
#
# return redirect('facebook_share_succeeded_page')
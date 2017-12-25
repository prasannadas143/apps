from django.conf import settings
from django.contrib.auth import get_backends
from django.contrib.auth import login
from django.dispatch import Signal
from .models import ParentChildUser
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User


# An admin has approved a user's account
user_approved = Signal(providing_args=["user", "request"])

# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])


def login_user(sender, user, request, **kwargs):
    """ Automatically authenticate the user when activated  """
    backend = get_backends()[0]  # Hack to bypass `authenticate()`.
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    request.session['REGISTRATION_AUTO_LOGIN'] = True
    request.session.modified = True

@receiver(post_delete, sender=User)
def cleanup_users(sender, **kwargs):
    userid=kwargs.get('instance').id
    pcobj = ParentChildUser.objects.filter( parentuser = userid )
    if pcobj.exists():
        pcobj[0].delete()

if getattr(settings, 'REGISTRATION_AUTO_LOGIN', False):
    user_activated.connect(login_user)

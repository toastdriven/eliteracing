from registration.backends.simple.views import RegistrationView

from accounts.forms import SignupForm


class CommanderRegistrationView(RegistrationView):
    form_class = SignupForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None and user.is_active:
                login(request, user)
                return redirect(
                    'cmdr_detail',
                    cmdr_name=user.commanders.first().name
                )

            # Either their credentials were invalid or their account has been
            # locked. Inform them in a general way.
            messages.add_message(
                request,
                messages.ERROR,
                'Invalid credentials or account is locked.'
            )
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
    })


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.create_user()
            return render(request, 'accounts/check_email.html', {
                'user': user,
            })
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
    })

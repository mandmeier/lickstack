from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(
                request, f'Your account has been created. You are now able to log in!')

            subject = "Welcome to the LickStack!"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            with open(settings.BASE_DIR + "/users/templates/users/sign_up_email.txt") as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template("users/sign_up_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()

            return redirect('login')
    else:
        form = UserRegisterForm()  # just empty form
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


@login_required
def delete_user(request):
    u = request.user
    email = u.email
    u.delete()
    logout(request)
    messages.success(request, "Your LickStack profile has been deleted")

    subject = "Your LickStack profile has been deleted"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    with open(settings.BASE_DIR + "/users/templates/users/delete_profile_email.txt") as f:
        signup_message = f.read()
    message = EmailMultiAlternatives(
        subject=subject, body=signup_message, from_email=from_email, to=to_email)
    html_template = get_template("users/delete_profile_email.html").render()
    message.attach_alternative(html_template, "text/html")
    message.send()

    return render(request, 'users/logout.html')

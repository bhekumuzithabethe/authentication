# Django imports for views and helpers
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required

# =============================
# Home Page View
# =============================
def home_view(request):
    # Retrieve any stored messages to display in the template (success/errors)
    messages_to_display = messages.get_messages(request)
    return render(request, 'registration/base.html', {
        'messages': messages_to_display,
    })

# =============================
# User Registration View
# =============================
def user_registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save user object but don't activate yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Prepare account activation email
            current_site = get_current_site(request)
            protocol = request.scheme  # Detect 'http' or 'https'
            email_subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])

            try:
                email.send()
                messages.success(request, 'Please check your email to complete the registration.')
                return redirect('home')
            except Exception as e:
                # Fallback if email fails
                messages.error(request, f'Email could not be sent: {e}')
                return redirect('sign-up')
        else:
            messages.error(request, 'Invalid form sent.')
            return redirect('sign-up')
    else:
        # GET request — present blank sign-up form
        form = RegistrationForm()
        return render(request, 'registration/sign_up.html', {'form': form})

# =============================
# Account Activation View
# =============================
def account_activation_view(request, uidb64, token):
    User = get_user_model()
    try:
        # Decode the UID from the activation URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    # Validate token and activate account
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)  # Log the user in after activation
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Your activation link is invalid or expired.')
        return redirect('home')

# =============================
# Login View
# =============================
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        User = get_user_model()
        if form.is_valid():
            # Get credentials from form
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            # Check user existence and credentials
            if User.objects.filter(email=email).exists() and User.objects.filter(password=password).exists:
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect('dologin')
            else:
                messages.error(request, "Username does not exist.")
                return redirect('dologin')
        else:
            messages.error(request, "Failed to login.")
            return redirect('dologin')
    else:
        # GET request — display the login form
        form = LoginForm()
        return render(request, "index.html", {'form': form})

# =============================
# Logout View
# =============================
@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')

# =============================
# Index View (Protected)
# =============================
@login_required()
def index_view(request):
    return render(request, 'index.html')
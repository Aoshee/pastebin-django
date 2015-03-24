from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from users.forms import RegisterForm, LoginForm
from users.models import Favorite

from pastes.models import Paste

def register_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated():
        # User is already authenticated
        return render(request, 'users/register/already_logged_in.html')
    else:
        register_form = RegisterForm(request.POST or None)
        
        if request.method == 'POST': # Form data was submitted
            if register_form.is_valid(): # Form data is valid
                # Create the user
                user = User.objects.create_user(register_form.cleaned_data['username'],
                                                "N/A", # we don't deal with email addresses
                                                register_form.cleaned_data['password'])
                                                  
                # TODO: Show a different message if the registration fails
                return render(request, 'users/register/register_success.html')
                
    # Show the registration page
    return render(request, "users/register/register.html", { "form": register_form })
    
def login_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated():
        # User is authenticated
        return render(request, "users/login/logged_in.html")
    else:
        login_form = LoginForm(request.POST or None)
        
        # User is NOT authenticated
        if request.method == 'POST': # Form data was submitted
            if login_form.is_valid(): # Form data is valid
                user = authenticate(username = login_form.cleaned_data['username'],
                                    password = login_form.cleaned_data['password'])
                
                if user is not None and user.is_active:
                    login(request, user)
                    return render(request, "users/login/logged_in.html")
                else:
                    # Couldn't authenticate, either the username or password is wrong
                    error = "User doesn't exist or the password is incorrect."
                    login_form._errors['password'] = login_form.error_class([error])
                    
    # Show the login form
    return render(request, "users/login/login.html", { "form": login_form })

def logout_view(request):
    """
    Logout the user and show the logout page
    """
    if request.user.is_authenticated():
        logout(request)
        
    return render(request, 'users/logout/logged_out.html')

def profile(request, username):
    """
    Show the user's profile, which shows his most recent favorites and uploaded pastes
    """
    profile_user = User.objects.get(username=username)
    
    if profile_user == None:
        return render(request, "users/profile/profile_error.html", {"reason": "not_found"})
    
    favorites = Favorite.get_favorites(profile_user, count=15)
    total_favorite_count = Favorite.get_favorite_count(profile_user)
    
    pastes = Paste.get_pastes(profile_user, count=15)
    total_paste_count = Paste.get_paste_count(profile_user)
    
    return render(request, "users/profile/profile.html", {"profile_username": profile_user.username,
                                                          "favorites": favorites,
                                                          "total_favorite_count": total_favorite_count,
                                                          
                                                          "pastes": pastes,
                                                          "total_paste_count": total_paste_count })
    
def pastes(request, username, page=1):
    """
    Show all of user's pastes
    """
    pass
    
def favorites(request, username, page=1):
    """
    Show all of user's favorites
    """
    pass
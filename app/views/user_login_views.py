from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, reverse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from app.models.user import MyUser
from app.models.user import UserLoginForm
from app.models.user import UserRegisterForm


def login_required_mine(func):
    def wraper(request, *args, **kwargs):
        has_login = request.COOKIES.get("Okaygis_id", None)
        if NewUser.objects.filter(id=has_login).count() == 0:
            return redirect('user_login')
        return func(request, *args, **kwargs)
    return wraper


def user_logout(request):
    logout(request)
    resp = HttpResponseRedirect(reverse('index'))
    return resp


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                rep = redirect(reverse('index'))
                return rep
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                MyUser.objects.create_user(username=data["username"], password=data["password"], email=data['email'],
                                           phone_number=data['phone_number'])
            except ValueError:
                return "something wrong happened, please try again"
            return HttpResponse(content=content)
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {"form": form})



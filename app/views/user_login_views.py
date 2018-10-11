from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, reverse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

from app.models.user import MyUser
from app.models.user import UserLoginForm
from app.models.user import UserRegisterForm


from app.utils import pass_hash


def login_required_mine(func):
    def wraper(request, *args, **kwargs):
        has_login = request.COOKIES.get("Okaygis_id", None)
        if NewUser.objects.filter(id=has_login).count() == 0:
            return redirect('user_login')
        return func(request, *args, **kwargs)
    return wraper


def logout(request):
    resp = HttpResponseRedirect(reverse('index'))
    resp.delete_cookie("Okaygis_id")
    return resp


def login(request):
    user_id = request.COOKIES.get('Okaygis_id', None)
    if MyUser.objects.filter(id=user_id):
        return redirect('index')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = MyUser.objects.filter(name=username).first()
            if user and check_password(password, user.password):
                rep = HttpResponseRedirect(reverse("index"))
                rep.set_cookie('Okaygis_id', user.id, max_age=60*60*24)
                return rep
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            content = save_user(form.cleaned_data)
            return HttpResponse(content=content)
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {"form": form})


def save_user(data):
    try:
        user = MyUser()
        user.name = data['name']
        user.password = make_password(data["password"])
        user.email = data["email"]
        user.phone_number = data['phone_number']
        user.save()
    except ValueError:
        return "something wrong happened, pleasse try again"
    return "Thanks"


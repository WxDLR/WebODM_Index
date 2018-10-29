from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, reverse
from django.shortcuts import render
from django.contrib.auth import login, logout
from app.models.user import MyUser
from app.models.user import UserLoginForm
from app.models.user import UserRegisterForm


def login_required(func):
    def wraper(request, *args, **kwargs):
        if not request.myuser:
            return redirect('user_login')
        return func(request, *args, **kwargs)
    return wraper


def user_logout(request):
    myuser = getattr(request, 'myuser', None)
    if myuser:
        myuser = None
    resp = HttpResponseRedirect(reverse('index'))
    resp.delete_cookie("Okaygis")
    return resp


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = MyUser.objects.filter(username=username).first()
            if user is not None and user.password == password:
                rep = redirect(reverse('index'))
                rep.set_cookie("Okaygis", user.id)
                return rep
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except ValueError:
                return "something wrong happened, please try again"
            return HttpResponse(content="ok")
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {"form": form})


@login_required
def user_detail(request):
    return render(request, 'app/Okaygis/mine.html')

import json

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction

from app.models import image_upload
from app.models.user import MyUser
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from guardian.shortcuts import get_objects_for_user

from nodeodm.models import ProcessingNode
from app.models import Project, Task
from django.contrib import messages
from django.utils.translation import ugettext as _

from django import forms
from app.api.projects import ProjectSerializer


def index(request):
    queryset = Project.objects.all()
    serialize = ProjectSerializer(queryset, many=True)
    # print(serialize.data)
    return render(request, 'Okaygis/index.html', context={"projects": serialize.data})


def model(request):
    queryset = Project.objects.all()
    serialize = ProjectSerializer(queryset, many=True)
    return render(request, 'Okaygis/model.html', context={"projects": serialize.data})


def dashboard(request):
    myuser = MyUser.objects.filter(id=request.COOKIES.get('Okaygis_id')).first()
    no_processingnodes = ProcessingNode.objects.count() == 0
    no_tasks = Task.objects.filter(project__owner=myuser).count() == 0

    # Create first project automatically
    if Project.objects.count() == 0:
        Project.objects.create(owner=myuser, name=_("First Project"))

    return render(request, 'app/dashboard.html', {
        'title': 'Dashboard',
        'no_processingnodes': no_processingnodes,
        'no_tasks': no_tasks
    })


def map(request, project_pk=None, task_pk=None):
    title = _("Map")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()
        
        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name
            mapItems = [task.get_map_items()]
        else:
            title = project.name
            mapItems = project.get_map_items()

    return render(request, 'app/map.html', {
            'title': title,
            'params': {
                'map-items': json.dumps(mapItems),
                'title': title,
                'public': 'false'
            }.items()
        })


# @login_required
def model_display(request, project_pk=None, task_pk=None):
    title = _("3D Model Display")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()

        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name
        else:
            raise Http404()

    return render(request, 'app/3d_model_display.html', {
            'title': title,
            'params': {
                'task': json.dumps(task.get_model_display_params()),
                'public': 'false'
            }.items()
        })


# @login_required
def processing_node(request, processing_node_id):
    pn = get_object_or_404(ProcessingNode, pk=processing_node_id)
    if not pn.update_node_info():
        messages.add_message(request, messages.constants.WARNING, '{} seems to be offline.'.format(pn))

    return render(request, 'app/processing_node.html', 
            {
                'title': 'Processing Node', 
                'processing_node': pn,
                'available_options_json': pn.get_available_options_json(pretty=True)
            })


class FirstUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'email')
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput,
        }


def welcome(request):
    if MyUser.objects.filter(is_superuser=True).count() > 0:
        return redirect('index')

    fuf = FirstUserForm()

    if request.method == 'POST':
        fuf = FirstUserForm(request.POST)
        if fuf.is_valid():
            admin_user = fuf.save(commit=False)
            admin_user.password = make_password(fuf.cleaned_data['password'])
            admin_user.is_superuser = admin_user.is_staff = True
            admin_user.save()

            # Log-in automatically
            # login(request, admin_user, 'django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

    return render(request, 'app/welcome.html',
                  {
                      'title': 'Welcome',
                      'firstuserform': fuf
                  })


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)

# MyViews
def models(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return render(request, 'models.html', context={'projectlist': serializer.data})


from app.models import ImageUpload
from app.api.tasks import TaskSerializer


def image_upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('img')
        for img in images:
            task = Task.objects.filter(id="20cf5374-02ca-4aa4-ada8-6b8375c719fa").first()
            image = ImageUpload(task=task, image=img)
            image.save()
        return HttpResponse(content="hello")
    else:
        return render(request, 'imageupload.html')


def task_test(request, project_pk=None):
    if request.method == "GET":
        # form = TaskForm()
        return render(request, 'imageupload.html')
    else:
        project = Project.objects.get(pk=project_pk)
        file_list = request.FILES.getlist(key="img")
        with transaction.atomic():
            task = Task.objects.create(project=project, )
            for file in file_list:
                ImageUpload.objects.create(task=task, image=file)
            task.name = request.POST.get('name')
            task.options = request.POST.get('options')
            task.save()
            return HttpResponse(status=200, content="Ok")


def model_details(request):
    return render(request, 'app/model_detail.html')
    pass



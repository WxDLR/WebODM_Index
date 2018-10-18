from django.db import models
from .task import Task, assets_directory_path


def upload_handler(image_upload, filename):
    return assets_directory_path(image_upload.task.id, image_upload.task.project.id, filename)


class ImageUp(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_handler)

    def __str__(self):
        return self.image.name

    def path(self):
        return self.image.path

from django.db import models
from ckeditor.fields import RichTextField
from common.models import MainModel, User


class Project(MainModel):
    name = models.CharField('名称', max_length=100, null=True, blank=True)
    content = RichTextField('描述', null=True, blank=True)
    code = models.TextField('代码', null=True, blank=True)
    start_date = models.DateField('开始时间', null=True, blank=True)
    end_date = models.DateField('结束时间', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name


class ProjectFiles(MainModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField('文件', upload_to='projects/', null=True, blank=True)
    sort = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "项目文件"
        verbose_name_plural = verbose_name


class ProjectUser(MainModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField('角色', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "参与人"
        verbose_name_plural = verbose_name


class PythonTrain(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField('代码', null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "python练习"
        verbose_name_plural = verbose_name


class ScratchTrain(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField('代码', null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "Scratch练习"
        verbose_name_plural = verbose_name

from django.db import models
from ckeditor.fields import RichTextField
from common.models import MainModel, User


class LessonType(MainModel):
    name = models.CharField('名称', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name


class Lesson(MainModel):
    lesson_type = models.ForeignKey(LessonType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("名称", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    url = models.CharField('连接', max_length=255, null=True, blank=True)
    sort = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


class HomeworkSubject(MainModel):
    title = models.CharField("标题", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    default_code = models.TextField('预设代码', null=True, blank=True)
    code = models.TextField('代码', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "练习题"
        verbose_name_plural = verbose_name


class LessonHomework(MainModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    homework_subject = models.ForeignKey(HomeworkSubject, on_delete=models.CASCADE, null=True, blank=True)
    sort = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.lesson.title

    class Meta:
        verbose_name = "课题作业"
        verbose_name_plural = verbose_name


class Homework(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    homework_subject = models.ForeignKey(HomeworkSubject, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField('作业内容', null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name

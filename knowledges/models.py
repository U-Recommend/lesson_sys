from django.db import models
from ckeditor.fields import RichTextField

from common.models import MainModel
from lessons.models import CODE_LANGUAGE


class Knowledge(MainModel):
    language = models.CharField('类型', max_length=30, choices=CODE_LANGUAGE, default="python")
    title = models.CharField('标题', max_length=40, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    sort = models.IntegerField('排序', default=0)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Python教程"
        verbose_name_plural = verbose_name


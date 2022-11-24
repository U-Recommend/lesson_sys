from django.db import models
from ckeditor.fields import RichTextField
from common.models import MainModel, User


class LessonType(MainModel):
    name = models.CharField('名称', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "类型"
        verbose_name_plural = verbose_name


class LessonTypeUser(MainModel):
    lesson_type = models.ForeignKey(LessonType, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "学生课程类型"
        verbose_name_plural = verbose_name


class Lesson(MainModel):
    lesson_type = models.ForeignKey(LessonType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("名称", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    url = models.CharField('连接', max_length=255, null=True, blank=True)
    pdf = models.FileField('PDF', upload_to="lessons/", null=True, blank=True)
    sort = models.IntegerField('排序', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


HOMEWORK_SUBJECT_HAS_CODE = (
    (0, "否"),
    (1, "是"),
)


class HomeworkSubject(MainModel):
    title = models.CharField("标题", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    default_code = models.TextField('预设代码', null=True, blank=True)
    code = models.TextField('代码', null=True, blank=True)
    has_code = models.IntegerField('是否需要代码', choices=HOMEWORK_SUBJECT_HAS_CODE, default=0)

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
    comment = RichTextField('老师评语', null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name


class LessonUser(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    lesson_date = models.DateField("上课时间", null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "考勤"
        verbose_name_plural = verbose_name

from django.db import models
from ckeditor.fields import RichTextField
from common.models import MainModel, User, Grade, STATUS

CODE_LANGUAGE = (
    ('', '-'),
    ('python', 'Python'),
    ('scratch', 'Scratch')
)


class Course(MainModel):
    title = models.CharField("名称", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    url = models.CharField('连接', max_length=255, null=True, blank=True)
    pdf = models.FileField('PDF', upload_to="lessons/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课件"
        verbose_name_plural = verbose_name


SUBJECT_HAS_CODE = (
    (0, "否"),
    (1, "是"),
)


class Exercises(MainModel):
    code_language = models.CharField('编程语言', max_length=50, choices=CODE_LANGUAGE, default="python")
    title = models.CharField("标题", max_length=100, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    default_code = models.TextField('预设代码', null=True, blank=True)
    answer = RichTextField('答案', null=True, blank=True)
    code = models.TextField('答案代码', null=True, blank=True)
    need_code = models.IntegerField('是否需要代码', choices=SUBJECT_HAS_CODE, default=1)
    need_answer = models.IntegerField('是否需要答题', choices=SUBJECT_HAS_CODE, default=1)
    status = models.IntegerField('状态', choices=STATUS, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "习题"
        verbose_name_plural = verbose_name


class Lesson(MainModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS, default=1)
    lesson_date = models.DateField("上课时间", null=True, blank=True)
    num = models.IntegerField('节次', default=1)
    user = models.ManyToManyField(User, related_name='lesson_users')
    exercises = models.ManyToManyField(Exercises, related_name='exercises_lesson', null=True, blank=True)

    def __str__(self):
        return self.course.title if self.course else str(self.id)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


class Homework(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField('作业代码', null=True, blank=True)
    content = models.TextField('作业内容', null=True, blank=True)
    comment = RichTextField('老师评语', null=True, blank=True)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name


class Attendance(MainModel):
    pass

    class Meta:
        verbose_name = "考勤"
        verbose_name_plural = verbose_name
